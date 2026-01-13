# anki-snapshot

Git-based version control for Anki collections. Track flashcard changes with human-readable diffs.

## Features

- 📦 Snapshot your Anki database to git
- 📝 Human-readable diffs showing card changes
- 🖼️ Clickable image links in terminal
- 🔍 Search notes and history
- 📊 Snapshot history with stats
- 🔄 Restore previous versions

## Requirements

- Anki (desktop)
- git & git-lfs
- sqlite3, perl

## Installation
```bash
git clone https://github.com/chrislongros/anki-snapshot.git
cd anki-snapshot
chmod +x anki-*
# Add to PATH
echo 'export PATH="$PWD:$PATH"' >> ~/.bashrc
```

## Usage
```bash
anki-snapshot              # Create snapshot (close Anki first)
anki-diff                  # Show changes since last snapshot
anki-diff HEAD~3..HEAD     # Show changes across 3 snapshots
anki-log                   # View snapshot history
anki-log 20                # Show more history
anki-search "mitochondria" # Find notes matching pattern
anki-search "mitochondria" --history  # Search git history
anki-restore               # Restore from snapshot (with confirmation)
```

## Auto-snapshot

Add to your Anki launch alias:
```bash
alias anki='/usr/bin/anki; anki-snapshot && anki-diff'
```

## Configuration

Environment variables:
- `ANKI_PROFILE` - Profile name (auto-detected if not set)
- `ANKI_SNAPSHOT_DIR` - Snapshot location (default: ~/anki-snapshot)

## License

MIT
