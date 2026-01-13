# anki-snapshot

Git-based version control for Anki collections. Track changes to your flashcards with human-readable diffs.

## Features

- 📦 Snapshot your Anki database to git
- 📝 Human-readable diffs showing card changes
- 🖼️ Clickable image links in diffs
- 🔄 Restore previous versions
- 💾 Uses git-lfs for media files

## Requirements

- Anki (desktop)
- git & git-lfs
- sqlite3, perl

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/anki-snapshot.git
cd anki-snapshot
chmod +x anki-snapshot anki-diff anki-restore
sudo ln -s "$PWD/anki-snapshot" /usr/local/bin/
sudo ln -s "$PWD/anki-diff" /usr/local/bin/
sudo ln -s "$PWD/anki-restore" /usr/local/bin/
```

## Usage
```bash
# Close Anki first, then:
anki-snapshot          # Create snapshot
anki-diff              # Show changes since last snapshot
anki-diff HEAD~3..HEAD # Show changes across 3 snapshots
anki-restore           # Restore from snapshot (with confirmation)
```

## Configuration

Environment variables:
- `ANKI_PROFILE` - Profile name (auto-detected if not set)
- `ANKI_SNAPSHOT_DIR` - Snapshot location (default: ~/anki-snapshot)

## License

MIT
