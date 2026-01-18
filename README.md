# anki-snapshot

Git-based version control for Anki collections. Track flashcard changes with human-readable diffs.

## Features

- 📦 **Snapshot** your Anki database to git
- 📝 **Human-readable diffs** showing field-by-field changes
- 🏷️ **Field names** and note types displayed (Text, Extra, Cloze-AI, etc.)
- 🖼️ **Clickable media links** in terminal (images, audio)
- 🔍 **Search** notes and git history
- 📊 **History** with change statistics
- 🔄 **Restore** previous versions

## Installation

### Bash (Linux/macOS/WSL)
```bash
git clone https://github.com/chrislongros/anki-snapshot.git
cd anki-snapshot/bash
chmod +x anki-*

# Option 1: Add to PATH
echo 'export PATH="$HOME/anki-snapshot/bash:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Option 2: Symlink to /usr/local/bin
sudo ln -s "$PWD"/anki-* /usr/local/bin/
```

**Arch Linux (AUR):**
```bash
yay -S anki-snapshot
```

### Python (Cross-platform)
```bash
pip install git+https://github.com/chrislongros/anki-snapshot.git#subdirectory=python
```

## Usage

### Take a Snapshot
```bash
anki-snapshot
```
```
📦 Copying database to temp...
📄 Exporting notes for diff...
📝 Committing...
✅ Done!
```

### View Changes
```bash
anki-diff                  # Changes since last snapshot
anki-diff HEAD~3..HEAD     # Changes across multiple commits
```
```
━━━ Anki Changes ━━━
2026-01-18 09:59:55 → 2026-01-18 10:01:24

━━━ Modified [Cloze-AI] ━━━
ID: 1768724713223
  Text:
    - this is a {{c1::new}} card.
    + this is a {{c1::new}} card. {{c2::with more clozes}}
  Extra:
    - [img:paste-1f6e89...png]
    + [img:paste-1f6e89...png] [img:paste-0b1f99...png]

━━━ Image Changes ━━━
Added:
  + paste-0b1f99...png
```

### View History
```bash
anki-log                   # Last 10 snapshots
anki-log 20                # Last 20 snapshots
```
```
━━━ Anki Snapshot History ━━━

📝 947c5f4 2026-01-18 10:19 Snapshot 2026-01-18 10:19 (+5/-3)
✅ 34f9efa 2026-01-18 10:12 Snapshot 2026-01-18 10:12 (+12/-0)
🗑️ 1b7d522 2026-01-18 10:07 Snapshot 2026-01-18 10:07 (+0/-8)
```

### Search Notes
```bash
anki-search "mitochondria"            # Search current notes
anki-search "mitochondria" --history  # Search git history
```
```
━━━ Notes Matching: mitochondria ━━━

[1486522758122] [Cloze-AI]
  Text: The {{c1::mitochondria}} is the powerhouse of the cell
  Extra: [img:mito-diagram...png] ATP production

[1489890842539] [Cloze-AI]
  Text: {{c1::Mitochondria}} have their own {{c2::DNA}}
```

### Restore
```bash
anki-restore
```

### Auto-snapshot with Anki

Use the wrapper to auto-snapshot when Anki closes:
```bash
# Add alias to your shell config
alias anki='anki-wrapper'
```

Or for development builds:
```bash
alias ankibuild='cd ~/ankidev/anki && ./tools/runopt; anki-snapshot && anki-diff'
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ANKI_PROFILE` | Anki profile name | Auto-detected |
| `ANKI_SNAPSHOT_DIR` | Snapshot location | `~/anki-snapshot` |

## Terminal Support

Clickable media links use [OSC 8 hyperlinks](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda). Supported terminals:

- ✅ Alacritty
- ✅ Kitty
- ✅ iTerm2
- ✅ WezTerm
- ✅ GNOME Terminal (3.26+)
- ✅ Windows Terminal

## Requirements

**Bash version:**
- git
- sqlite3
- bash 4.0+ (for associative arrays)

**Python version:**
- git
- Python 3.8+

## How It Works

1. Copies Anki database to a temp file (never modifies original)
2. Exports notes as `notes.txt` with format: `id|model_id|field1|field2|...|tags`
3. Commits to git repository
4. Diffs show field-by-field changes with note type and field names

No personal data is stored in the git repo - only `notes.txt` is tracked.

## License

MIT

## Screenshots

<img width="2560" height="919" alt="anki-snapshot diff output" src="https://github.com/user-attachments/assets/f182a7f3-48af-4ab8-b466-483b15188968" />
