#!/usr/bin/env bash
# backup.sh - timestamped .tar.gz backup, keeps only the newest N.
# Usage: backup.sh <source_dir> <backup_dir> [keep=7]
set -euo pipefail

SRC="${1:-}"; DEST="${2:-}"; KEEP="${3:-7}"

if [[ -z "$SRC" || -z "$DEST" ]]; then
  echo "Usage: $0 <source_dir> <backup_dir> [keep]" >&2; exit 2
fi
if [[ ! -d "$SRC" ]]; then
  echo "ERROR: source '$SRC' is not a directory" >&2; exit 1
fi

mkdir -p "$DEST"
STAMP="$(date +%Y-%m-%d_%H-%M-%S)"
NAME="$(basename "$SRC")"
ARCHIVE="$DEST/${NAME}_${STAMP}.tar.gz"

echo "[$(date '+%F %T')] Backing up $SRC -> $ARCHIVE"
tar -czf "$ARCHIVE" -C "$(dirname "$SRC")" "$NAME"

if tar -tzf "$ARCHIVE" > /dev/null; then
  echo "[$(date '+%F %T')] OK: $(du -h "$ARCHIVE" | cut -f1) written"
else
  echo "ERROR: archive verification failed" >&2; exit 1
fi

ls -1t "$DEST/${NAME}_"*.tar.gz | tail -n +$((KEEP + 1)) | xargs -r rm -f --
echo "[$(date '+%F %T')] Done. Keeping last $KEEP backups."
