# Bash Scripts — Automation & Scheduling

This folder holds all the Bash scripts from Week 2, Day 4 (Bash Scripting). The goal of the day was to learn script structure, control flow, cron scheduling, and how Bash and Python can call each other — then prove it all works with a real backup + cron job.

## What's in this folder

| File | Purpose |
|---|---|
| `bash_basics.sh` | Practice: shebang, variables, input/output, conditions, loops |
| `backup.sh` | Creates a timestamped `.tar.gz` backup and keeps only the newest N |
| `crontab.txt` | The cron entry that runs `backup.sh` automatically every day at 2 AM |
| `run_monitoring.sh` | Bash script that runs the Week 2 Python scripts and reacts to their exit codes |
| `py_calls_bash.py` | Python script that calls `backup.sh` using `subprocess` |
| `README.md` | This file |

## Requirements

- Bash (comes with WSL2/Ubuntu)
- `cron` installed and running (`sudo apt install cron`, `sudo service cron start`)
- Python virtual environment set up at the repo root (`.venv`), with `requests` installed — needed by `run_monitoring.sh`

---

## 1. `bash_basics.sh`

A warm-up script. Nothing here gets used later — it just proves I can write the core building blocks of Bash without looking them up.

**What it covers:**
- The shebang line (`#!/usr/bin/env bash`) — tells Linux which program should run this file
- Variables (`NAME="$(whoami)"`)
- Input from the user (`read -rp`)
- Output (`echo`)
- `if / elif / else` conditions
- `for` and `while` loops
- Script arguments (`$0`, `$1`, `$#`)

**How to run it:**

```bash
chmod +x bash_basics.sh
./bash_basics.sh hello
```

**Example output:**

```
<paste your output here>
```

**What I learned:** Bash uses `$(...)` instead of Python's `f"{...}"`. Also, spacing matters a lot in Bash — `NAME = "x"` (with spaces around `=`) is actually a syntax error, but `NAME="x"` is fine.

---

## 2. `backup.sh`

**What it does:**
- Takes a source folder, a destination folder, and how many backups to keep (in that order)
- Creates a timestamped `.tar.gz` archive of the source folder
- Verifies the archive isn't corrupted by test-reading it right after creating it
- Deletes the oldest backups once there are more than the number you asked to keep
- Prints a timestamped message for every step, so the log file makes sense on its own

**Usage:**

```bash
./backup.sh <source_dir> <backup_dir> [keep=7]
```

**Example run and output:**

```bash
mkdir -p ~/backup-test/data && echo "hello cloud" > ~/backup-test/data/a.txt
./backup.sh ~/backup-test/data ~/backup-test/backups 3
```

```
[2026-09-22 17:09:42] Backing up /home/tanzeelsid/backup-test/data -> /home/tanzeelsid/backup-test/backups/data_2026-09-22_17-09-42.tar.gz
[2026-09-22 17:09:42] OK: 4.0K written
[2026-09-22 17:09:42] Done. Keeping last 3 backups.
```

After running it 4 times, only the newest 3 archives remain:

```bash
ls -l ~/backup-test/backups
```

```
data_2026-09-22_17-08-55.tar.gz
data_2026-09-22_17-09-42.tar.gz
data_2026-09-22_17-10-16.tar.gz
```

**How it works, step by step:**

1. Checks that a source and destination were given, and that the source is a real folder. Exits with an error if not.
2. Builds a filename using the current date and time (`date +%Y-%m-%d_%H-%M-%S`), so every backup has a unique name.
3. Runs `tar -czf` to compress the source folder into one `.tar.gz` file.
4. Runs `tar -tzf` right after, just to list the contents — if this fails, the archive is broken, and the script stops with an error instead of pretending it worked.
5. Lists all existing backups from newest to oldest (`ls -1t`), skips the first `KEEP` of them, and deletes everything after that (`xargs -r rm -f`).

**Error handling:**

| Problem | What happens |
|---|---|
| No source/destination given | Prints usage message, exits with code `2` |
| Source folder doesn't exist | Prints an error, exits with code `1` |
| Archive fails the verification read | Prints an error, exits with code `1` |
| `set -euo pipefail` at the top | Stops the script immediately on any unexpected command failure, instead of continuing with a half-broken backup |

**Exit codes:** `0` = success, `1` = backup or verification failed, `2` = bad usage.

---

## 3. Cron job — automatic daily backup at 2 AM

**Why cron:** a backup script only helps if it actually runs without me remembering to do it. Cron is Linux's built-in job scheduler.

**Cron syntax:** `minute hour day-of-month month day-of-week`. `0 2 * * *` means "at minute 0, hour 2, every day."

**How I set it up:**

1. Made sure cron was running: `sudo service cron start`
2. Tested with a 1-minute schedule first (`* * * * *`) to prove the command actually works, before trusting it to a schedule I can't watch live
3. Confirmed new backups were appearing every minute in `~/backup-test/backups`, and that only the last 3 were being kept
4. Replaced the test line with the real 2 AM schedule
5. Saved the final crontab into `crontab.txt` in this folder as proof

**The final entry (also saved in `crontab.txt`):**

```
0 2 * * * /home/tanzeelsid/Desktop/myfolder/cloud-engineering-journey/week-02/bash-scripts/backup.sh /home/tanzeelsid/backup-test/data /home/tanzeelsid/backup-test/backups 7 >> /home/tanzeelsid/backup-test/backup.log 2>&1
```

**Why I used full paths everywhere:** cron doesn't load my normal shell environment, so `~` and relative paths aren't reliable. Absolute paths avoid that problem completely.

**How I verified it, without waiting until 2 AM:**

```bash
crontab -l                          # confirms the entry is installed
tail ~/backup-test/backup.log       # shows the script's own timestamped messages
ls -l ~/backup-test/backups         # confirms new archives are appearing
```

I proved the mechanism works using the 1-minute test schedule. The 2 AM run itself only fires if the machine is on at 2 AM — I'll check `backup.log` tomorrow morning to confirm it fired for real.

---

## 4. Combining Python and Bash

Two scripts show both directions of this combination.

### `run_monitoring.sh` — Bash calls Python and reacts to its exit code

**What it does:** runs the Week 2 Python scripts (website checker, log parser) and checks their exit codes. If either one signals a problem, it prints an `ALERT` line.

**How to run it:**

```bash
./run_monitoring.sh; echo "exit: $?"
```

**Example output:**

```
== Website check ==
<paste your output here>
== Log parse ==
<paste your output here>
ALERT: checker exit=1, parser exit=0
exit: 1
```

The website checker exits with `1` on purpose today — two of the test URLs in `urls.txt` are deliberately broken, so I can see the alert logic actually trigger.

**How it works:** it runs each Python script through the repo's virtual environment (`.venv/bin/python`), stores each script's exit code in a variable right after it runs (`$?`), and if either code isn't `0`, it prints an alert and exits `1` itself.

### `py_calls_bash.py` — Python calls Bash

**What it does:** uses Python's `subprocess.run()` to call `backup.sh` directly, capturing its output and exit code, instead of running it by hand in the terminal.

**How to run it:**

```bash
python py_calls_bash.py
```

**Example output:**

```
exit code: 0
[2026-09-22 ...] Backing up ...
[2026-09-22 ...] OK: ... written
[2026-09-22 ...] Done. Keeping last 3 backups.
```

**Why this matters:** it shows both directions of automation — Bash orchestrating Python scripts, and Python orchestrating Bash scripts. Real DevOps pipelines often mix both.

---

## Files and what to check before committing

| File | Committed? | Notes |
|---|---|---|
| `bash_basics.sh` | Yes | |
| `backup.sh` | Yes | |
| `crontab.txt` | Yes | Proof the cron entry exists |
| `run_monitoring.sh` | Yes | |
| `py_calls_bash.py` | Yes | |
| `~/backup-test/` | **No** | Test data lives outside the repo, ignored on purpose |
| `backup.log` | **No** | Log file, not source code |

## What I learned

- Cron doesn't use my normal shell environment, so every path in a crontab line has to be absolute
- Testing a cron schedule with `* * * * *` first is much faster than waiting to see if a daily job works
- `set -euo pipefail` catches mistakes early instead of letting a script silently do the wrong thing
- Bash and Python can call each other cleanly: Bash uses `$?` for exit codes, Python uses `subprocess.run()`

## Ideas for later

- Have `run_monitoring.sh` send a real alert (email/Slack) instead of just printing one
- Compress backups with a retention policy based on age, not just count
- Move `backup.log` rotation into `log_cleanup.sh` (added in Block 6)

---

**Note:** this README will be extended in Block 6 with three more scripts — `disk_monitor.sh`, `log_cleanup.sh`, and `health_check.sh`.
