#!/usr/bin/env bash
# run_monitoring.sh - Bash orchestrates the Python scripts and reacts to their exit codes
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PY="$REPO/.venv/bin/python"
CHK="$REPO/week-02/python-automation/website-checker"
PRS="$REPO/week-02/python-automation/log-parser"

echo "== Website check =="
"$PY" "$CHK/website_checker.py" --file "$CHK/urls.txt" --rounds 1
CHK_RC=$?

echo "== Log parse =="
"$PY" "$PRS/log-parser.py" "$PRS/sample.log" --max-errors 5
PRS_RC=$?

if [[ $CHK_RC -ne 0 || $PRS_RC -ne 0 ]]; then
  echo "ALERT: checker exit=$CHK_RC, parser exit=$PRS_RC"; exit 1
fi
echo "All good"
