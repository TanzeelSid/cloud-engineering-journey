# Week 2 — Python, Bash & Git Automation

This week covers Python fundamentals, cloud-relevant Python (APIs, JSON, error handling), automation scripts, Bash scripting with cron, and the full Git branch → PR → merge workflow.

## What's in this week

| File | What it does |
|---|---|
| `python-basics/logic_problems.py` | 10 small Python logic problems (fizzbuzz, palindrome check, prime check, word count, etc.) |
| `python-cloud/api_demo.py` | Calls the GitHub public API, parses the JSON response, and prints 3 fields |
| `python-automation/website-checker/website_checker.py` | Checks a list of websites and reports UP/DOWN status with an uptime summary |
| `python-automation/log-parser/log_parser.py` | Reads a log file and summarizes error counts and the most common error messages |
| `bash-scripts/bash_basics.sh` | Practice script: variables, input/output, conditions, loops |
| `bash-scripts/backup.sh` | Creates a timestamped `.tar.gz` backup and keeps only the newest N backups |
| `bash-scripts/crontab.txt` | Cron entry that runs `backup.sh` automatically every day at 2 AM |
| `bash-scripts/run_monitoring.sh` | Runs the Python checker/parser scripts and alerts based on their exit codes |
| `bash-scripts/py_calls_bash.py` | Calls `backup.sh` from Python using `subprocess` |
| `git-practice/NOTES.md` | Notes on a deliberate merge conflict I created and resolved |
| `bash-scripts/disk_monitor.sh` | Warns when any filesystem is above a usage threshold |
| `bash-scripts/log_cleanup.sh` | Deletes old `.log` files (dry-run by default for safety) |
| `bash-scripts/health_check.sh` | Checks disk, memory, CPU load, an HTTP endpoint, and cron status |

## Skills practiced

- Python: variables, conditionals, loops, functions, file I/O, JSON, `requests`, environment variables, `try/except`
- Bash: script structure, variables, conditions, loops, cron scheduling
- Git: `init`, `clone`, `add`, `commit`, `push`, `pull`, branching, merging, conflict resolution, pull requests

