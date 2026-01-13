#!/usr/bin/env python3
"""Git-based version control for Anki collections."""

import sqlite3
import subprocess
import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
YELLOW = "\033[0;33m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def get_anki_dir():
    xdg = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    anki_base = xdg / "Anki2"
    profile = os.environ.get("ANKI_PROFILE") or next(
        (p.name for p in anki_base.iterdir() 
         if p.is_dir() and p.name not in ("addons21", "addons")), None)
    if not profile:
        print(f"{RED}❌ No Anki profile found{RESET}")
        sys.exit(1)
    return anki_base / profile


def get_backup_dir():
    return Path(os.environ.get("ANKI_SNAPSHOT_DIR", Path.home() / "anki-snapshot"))


def is_anki_running():
    try:
        r1 = subprocess.run(["pgrep", "-x", "anki"], capture_output=True)
        r2 = subprocess.run(["pgrep", "-f", "aqt"], capture_output=True)
        return r1.returncode == 0 or r2.returncode == 0
    except FileNotFoundError:
        # Windows fallback
        result = subprocess.run(["tasklist"], capture_output=True, text=True)
        return "anki" in result.stdout.lower()


def init_repo(backup_dir):
    """Initialize git repo with LFS."""
    subprocess.run(["git", "init"], cwd=backup_dir)
    subprocess.run(["git", "lfs", "install"], cwd=backup_dir)
    extensions = ["png", "jpg", "jpeg", "gif", "mp3", "wav", "mp4", "webp", "svg"]
    gitattributes = "\n".join(
        f"*.{ext} filter=lfs diff=lfs merge=lfs -text" for ext in extensions
    )
    (backup_dir / ".gitattributes").write_text(gitattributes)


def export_notes(db_path, output_path):
    """Export notes to human-readable format."""
    conn = sqlite3.connect(db_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for row in conn.execute("SELECT id, mid, flds, tags FROM notes ORDER BY id"):
            note_id, model_id, fields, tags = row
            # Replace field separator
            fields = fields.replace("\x1f", " | ")
            # Preserve image references
            fields = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'[IMG:\1]', fields)
            # Strip other HTML
            fields = re.sub(r'<[^>]*>', '', fields)
            # Decode entities
            for old, new in [("&nbsp;", " "), ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&")]:
                fields = fields.replace(old, new)
            f.write(f"{note_id}|{model_id}|{fields}|{tags}\n")
    conn.close()


def snapshot():
    """Create a snapshot of the Anki collection."""
    if is_anki_running():
        print(f"{YELLOW}⚠️  Close Anki first!{RESET}")
        return False
    
    anki_dir = get_anki_dir()
    backup_dir = get_backup_dir()
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    if not (backup_dir / ".git").exists():
        init_repo(backup_dir)
    
    print(f"{BOLD}📦 Copying database...{RESET}")
    src = anki_dir / "collection.anki2"
    dst = backup_dir / "collection.anki2"
    dst.write_bytes(src.read_bytes())
    
    print(f"{BOLD}📄 Exporting notes...{RESET}")
    export_notes(dst, backup_dir / "notes.txt")
    
    print(f"{BOLD}📝 Committing...{RESET}")
    subprocess.run(["git", "add", "-A"], cwd=backup_dir)
    msg = f"Snapshot {datetime.now():%Y-%m-%d %H:%M}"
    result = subprocess.run(["git", "commit", "-m", msg], cwd=backup_dir, capture_output=True)
    if result.returncode != 0 and b"nothing to commit" in result.stderr:
        print(f"{DIM}No changes{RESET}")
    
    print(f"{GREEN}✅ Done!{RESET}")
    subprocess.run(["git", "log", "--oneline", "-3"], cwd=backup_dir)
    return True


def diff(range_spec="HEAD~1..HEAD"):
    """Show changes between snapshots."""
    backup_dir = get_backup_dir()
    media_dir = get_anki_dir() / "collection.media"
    
    print(f"{BOLD}━━━ Anki Changes: {range_spec} ━━━{RESET}\n")
    
    result = subprocess.run(
        ["git", "diff", range_spec, "--", "notes.txt"],
        cwd=backup_dir, capture_output=True, text=True
    )
    
    added_imgs, removed_imgs = set(), set()
    
    for line in result.stdout.splitlines():
        if line.startswith(("diff", "index", "---", "+++")):
            continue
        if line.startswith("@@"):
            print(f"\n{CYAN}────────────────────────────────────────{RESET}")
            continue
        
        if line.startswith("+"):
            content = line[1:]
            parts = content.split("|")
            if len(parts) >= 3:
                note_id, fields = parts[0], "|".join(parts[2:])
                # Track images
                for img in re.findall(r'\[IMG:([^\]]+)\]', fields):
                    added_imgs.add(img)
                # Shorten display
                fields = re.sub(r'\[IMG:([^\]]+)\]', r'[🖼 \1]', fields)
                if len(fields) > 150:
                    fields = fields[:150] + "..."
                print(f"{GREEN}+ [{note_id}] {fields}{RESET}")
        elif line.startswith("-"):
            content = line[1:]
            parts = content.split("|")
            if len(parts) >= 3:
                note_id, fields = parts[0], "|".join(parts[2:])
                for img in re.findall(r'\[IMG:([^\]]+)\]', fields):
                    removed_imgs.add(img)
                fields = re.sub(r'\[IMG:([^\]]+)\]', r'[🖼 \1]', fields)
                if len(fields) > 150:
                    fields = fields[:150] + "..."
                print(f"{RED}− [{note_id}] {fields}{RESET}")
    
    # Image changes
    print(f"\n{YELLOW}━━━ Image Changes ━━━{RESET}")
    new_imgs = added_imgs - removed_imgs
    del_imgs = removed_imgs - added_imgs
    
    if new_imgs:
        print(f"{GREEN}Added:{RESET}")
        for img in new_imgs:
            print(f"  {GREEN}+ {img}{RESET}")
            print(f"    file://{media_dir}/{img}")
    if del_imgs:
        print(f"{RED}Removed:{RESET}")
        for img in del_imgs:
            print(f"  {RED}− {img}{RESET}")
    if not new_imgs and not del_imgs:
        print(f"{DIM}  No image changes{RESET}")


def log(count=10):
    """Show snapshot history."""
    backup_dir = get_backup_dir()
    print(f"{BOLD}━━━ Anki Snapshot History ━━━{RESET}\n")
    
    result = subprocess.run(
        ["git", "log", "--oneline", "-n", str(count), "--format=%h %s"],
        cwd=backup_dir, capture_output=True, text=True
    )
    
    for line in result.stdout.strip().splitlines():
        hash_id, msg = line.split(" ", 1)
        stats = subprocess.run(
            ["git", "diff", "--shortstat", f"{hash_id}^..{hash_id}", "--", "notes.txt"],
            cwd=backup_dir, capture_output=True, text=True
        ).stdout
        added = re.search(r'(\d+) insertion', stats)
        removed = re.search(r'(\d+) deletion', stats)
        added = added.group(1) if added else "0"
        removed = removed.group(1) if removed else "0"
        
        if int(added) > 0 and int(removed) > 0:
            symbol = "📝"
        elif int(added) > 0:
            symbol = "✅"
        elif int(removed) > 0:
            symbol = "🗑️"
        else:
            symbol = "○"
        
        print(f"{symbol} {YELLOW}{hash_id}{RESET} {msg} {DIM}(+{added}/-{removed}){RESET}")
    
    print(f"\n{DIM}Usage: anki-snapshot diff <hash>~1..<hash>{RESET}")


def search(query, history=False):
    """Search notes."""
    backup_dir = get_backup_dir()
    
    if history:
        print(f"{BOLD}━━━ History Search: {YELLOW}{query}{RESET} {BOLD}━━━{RESET}\n")
        subprocess.run(
            ["git", "log", "--all", "-p", "-S", query, "--", "notes.txt"],
            cwd=backup_dir
        )
    else:
        print(f"{BOLD}━━━ Notes Matching: {YELLOW}{query}{RESET} {BOLD}━━━{RESET}\n")
        notes_file = backup_dir / "notes.txt"
        count = 0
        with open(notes_file, encoding="utf-8") as f:
            for line in f:
                if query.lower() in line.lower():
                    parts = line.split("|")
                    if len(parts) >= 3:
                        note_id = parts[0]
                        fields = "|".join(parts[2:])[:120]
                        # Highlight match
                        highlighted = re.sub(
                            f'({re.escape(query)})',
                            f'{YELLOW}\\1{RESET}',
                            fields,
                            flags=re.IGNORECASE
                        )
                        print(f"{DIM}[{note_id}]{RESET} {highlighted}")
                        count += 1
                        if count >= 20:
                            break
        print(f"\n{DIM}Found {count}+ matches. Use --history for git history.{RESET}")


def restore():
    """Restore from snapshot."""
    if is_anki_running():
        print(f"{YELLOW}⚠️  Close Anki first!{RESET}")
        return False
    
    anki_dir = get_anki_dir()
    backup_dir = get_backup_dir()
    
    print(f"{YELLOW}⚠️  This will OVERWRITE your Anki database!{RESET}")
    print(f"   Source: {backup_dir / 'collection.anki2'}")
    print(f"   Target: {anki_dir / 'collection.anki2'}")
    
    confirm = input("Type 'yes' to confirm: ")
    if confirm != "yes":
        print("Cancelled.")
        return False
    
    # Backup current
    print(f"{BOLD}💾 Backing up current...{RESET}")
    src = anki_dir / "collection.anki2"
    bak = anki_dir / f"collection.anki2.bak-{int(datetime.now().timestamp())}"
    bak.write_bytes(src.read_bytes())
    
    # Restore
    print(f"{BOLD}📦 Restoring...{RESET}")
    src.write_bytes((backup_dir / "collection.anki2").read_bytes())
    
    print(f"{GREEN}✅ Restored!{RESET}")
    return True


def main():
    commands = {
        "snapshot": (snapshot, "Create a snapshot"),
        "diff": (lambda *a: diff(a[0] if a else "HEAD~1..HEAD"), "Show changes"),
        "log": (lambda *a: log(int(a[0]) if a else 10), "Show history"),
        "search": (lambda *a: search(a[0], "--history" in a), "Search notes"),
        "restore": (restore, "Restore from snapshot"),
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(f"{BOLD}anki-snapshot{RESET} - Git-based Anki version control\n")
        print("Commands:")
        for cmd, (_, desc) in commands.items():
            print(f"  {GREEN}{cmd}{RESET}  {desc}")
        print(f"\nUsage: {sys.argv[0]} <command> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands[cmd][0](*args)


if __name__ == "__main__":
    main()
