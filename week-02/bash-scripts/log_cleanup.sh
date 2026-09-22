#!/usr/bin/env bash
# log_cleanup.sh - delete *.log files older than N days. DRY RUN unless --delete is given.
# Usage: log_cleanup.sh <log_dir> [days=7] [--delete]
set -euo pipefail

DIR="${1:-}"; DAYS="${2:-7}"; MODE="${3:-}"

if [[ -z "$DIR" || ! -d "$DIR" ]]; then
  echo "Usage: $0 <log_dir> [days] [--delete]" >&2; exit 2
fi
[[ "$DAYS" =~ ^[0-9]+$ ]] || { echo "days must be a number" >&2; exit 2; }

DIR="$(cd "$DIR" && pwd)"
case "$DIR" in
  /|/etc|/usr|/bin|/home|"$HOME") echo "Refusing to clean protected dir: $DIR" >&2; exit 2 ;;
esac

mapfile -t FILES < <(find "$DIR" -maxdepth 1 -type f -name "*.log" -mtime +"$DAYS")

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No .log files older than $DAYS days in $DIR"; exit 0
fi

for f in "${FILES[@]}"; do
  if [[ "$MODE" == "--delete" ]]; then rm -f -- "$f"; echo "Deleted: $f"
  else echo "Would delete: $f"; fi
done
[[ "$MODE" == "--delete" ]] || echo "Dry run only. Re-run with --delete to remove ${#FILES[@]} file(s)."
