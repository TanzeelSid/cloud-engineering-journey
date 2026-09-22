#!/usr/bin/env bash
# health_check.sh - quick system + endpoint health report. Exit 1 if any check fails.
# Usage: health_check.sh [url=https://example.com] [disk_max=90] [mem_max=90]
set -uo pipefail
URL="${1:-https://example.com}"; DISK_MAX="${2:-90}"; MEM_MAX="${3:-90}"
FAIL=0

check() {  # $1=label  $2=0(ok)/non-0(fail)  $3=detail
  if [[ "$2" -eq 0 ]]; then echo "[PASS] $1 - $3"; else echo "[FAIL] $1 - $3"; FAIL=1; fi
}

disk=$(df -P / | awk 'NR==2 {gsub("%","",$5); print $5}')
[[ "$disk" -lt "$DISK_MAX" ]]; check "Disk /" $? "${disk}% used (limit ${DISK_MAX}%)"

mem=$(free | awk '/^Mem:/ {printf "%d", $3/$2*100}')
[[ "$mem" -lt "$MEM_MAX" ]]; check "Memory" $? "${mem}% used (limit ${MEM_MAX}%)"

cores=$(nproc); load=$(awk '{print $1}' /proc/loadavg)
awk -v l="$load" -v c="$cores" 'BEGIN{exit !(l < c)}'; check "CPU load" $? "load $load on $cores core(s)"

code=$(curl -s -o /dev/null -m 10 -w "%{http_code}" "$URL" || true)
[[ "$code" =~ ^[23] ]]; check "HTTP $URL" $? "status ${code:-none}"

pgrep -x cron > /dev/null; rc=$?
check "cron process" $rc "$([[ $rc -eq 0 ]] && echo running || echo 'not running')"

echo
if [[ $FAIL -eq 0 ]]; then echo "OVERALL: HEALTHY"; else echo "OVERALL: UNHEALTHY"; fi
exit $FAIL
