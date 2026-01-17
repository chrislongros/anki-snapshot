# anki-snapshot

Git-based version control for Anki collections. Track flashcard changes with human-readable diffs.

## Features

- 📦 Snapshot your Anki database to git
- 📝 Human-readable diffs showing card changes
- 🖼️ Clickable image links in terminal
- 🔍 Search notes and history
- 📊 Snapshot history with stats
- 🔄 Restore previous versions

## Installation

### Bash (Linux/macOS/WSL)
```bash
git clone https://github.com/chrislongros/anki-snapshot.git
cd anki-snapshot/bash
chmod +x anki-*
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

### Bash
```bash
anki-snapshot              # Create snapshot
anki-diff                  # Show changes
anki-diff HEAD~3..HEAD     # Show changes across commits
anki-log                   # View history
anki-log 20                # More history
anki-search "mitochondria" # Search notes
anki-search "mitochondria" --history
anki-restore               # Restore from snapshot
```

### Python
```bash
anki-snapshot snapshot
anki-snapshot diff
anki-snapshot diff HEAD~3..HEAD
anki-snapshot log
anki-snapshot log 20
anki-snapshot search "mitochondria"
anki-snapshot search "mitochondria" --history
anki-snapshot restore
```

## Configuration

Environment variables:
- `ANKI_PROFILE` - Profile name (auto-detected if not set)
- `ANKI_SNAPSHOT_DIR` - Snapshot location (default: ~/anki-snapshot)

## Requirements

- **Bash:** git, git-lfs, sqlite3, perl
- **Python:** git, git-lfs, Python 3.8+

## License

MIT

## Screenshots

<img width="2560" height="919" alt="Screenshot_20260117_120737" src="https://github.com/user-attachments/assets/f182a7f3-48af-4ab8-b466-483b15188968" />


