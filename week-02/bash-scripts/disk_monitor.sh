#!/usr/bin/env bash
# disk_monitor.sh - warn when any filesystem is above a usage threshold.
# Usage: disk_monitor.sh [threshold_percent=80]
set -uo pipefail
THRESHOLD="${1:-80}"
ALERT=0

if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]]; then
  echo "Threshold must be a number" >&2; exit 2
fi

echo "Disk usage check (threshold ${THRESHOLD}%) - $(date '+%F %T')"
while read -r fs size used avail pct mount; do
  usage="${pct%\%}"
  if (( usage >= THRESHOLD )); then
    echo "WARNING: $mount is ${usage}% full ($used of $size used, $avail free)"
    ALERT=1
  else
    echo "OK:      $mount is ${usage}% full"
  fi
done < <(df -hP -x tmpfs -x devtmpfs -x squashfs | tail -n +2)

exit $ALERT
