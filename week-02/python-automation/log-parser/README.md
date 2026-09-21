# Log Parser

A small Python script that reads a log file and gives you a quick summary. Instead of scrolling through thousands of lines, you can see how many errors happened, how bad it is, and which error keeps repeating.

Log reading is a daily task for cloud and DevOps engineers, so this script automates the first step of it.

## What it does

- Reads a text log file line by line
- Counts how many lines belong to each level: CRITICAL, ERROR, WARN, INFO, DEBUG
- Calculates the error rate (percentage of lines that are errors)
- Shows the top repeated error messages
- Can save the summary to a file
- Can exit with code `1` when there are too many errors, so other scripts can react to it

## Requirements

- Python 3 only. No extra libraries to install, because it only uses the standard library (`argparse`, `re`, `sys`, `collections`).

## Log format it understands

The script looks for a level word (like `ERROR` or `INFO`) anywhere in each line. A typical line looks like this:

```
2026-09-20 08:02:30 ERROR Database connection failed
```

`sample.log` in this folder is a small example file you can test with.

## How to use it

Basic run:

```bash
python log_parser.py sample.log
```

Show the top 5 errors and save the summary to a file:

```bash
python log_parser.py sample.log --top 5 --out summary.txt
```

Fail (exit code 1) if there are more than 2 error lines:

```bash
python log_parser.py sample.log --max-errors 2
echo "exit code: $?"
```

Try it on a real Linux log:

```bash
python log_parser.py /var/log/syslog
```

## Options

| Option | Default | What it does |
|---|---|---|
| `logfile` | (required) | The path of the log file to read |
| `--top` | `3` | How many of the most common errors to show |
| `--out` | none | Also save the summary into this file |
| `--max-errors` | none | Exit with code `1` if error lines are more than this number |

## Example output

Running `python log_parser.py sample.log`:

```
Log summary: sample.log
Total lines: 12
  CRITICAL 1
  ERROR    4
  WARN     2
  INFO     5
Error rate: 41.7% (5 error lines)
Top 3 errors:
  3x  Database connection failed
  1x  Timeout calling payment API
  1x  Out of memory
```

How to read this:

- The file has 12 lines in total.
- 5 of them are serious (4 ERROR + 1 CRITICAL), so the error rate is 5 ÷ 12 = 41.7%.
- "Database connection failed" happened 3 times. That is the first thing I would investigate.

## How it works (step by step)

1. The script opens the log file and reads it one line at a time.
2. It skips empty lines.
3. A regular expression finds the level word in each line (`CRITICAL`, `ERROR`, `WARN`, `WARNING`, `INFO`, `DEBUG`). `WARNING` is counted as `WARN`.
4. Lines with no known level are counted as `OTHER`.
5. For `ERROR` and `CRITICAL` lines, the message after the level word is saved in a counter.
6. At the end it prints the totals, the error rate, and the most common error messages.
7. If `--out` is used, the same summary is written to a file.
8. If `--max-errors` is used and there are more error lines than that number, the script exits with code `1`.

## Error handling

| Problem | What the script does |
|---|---|
| Log file does not exist | Prints a clear message and exits with code `2` |
| No permission to read the file | Prints a clear message and exits with code `2` |
| Strange characters in the file | Replaces them instead of crashing |
| Empty file | Shows 0 lines and 0% error rate (no divide-by-zero crash) |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Summary printed. Everything is fine |
| `1` | Error lines are above the `--max-errors` limit |
| `2` | The log file is missing or cannot be read |

## Files in this folder

| File | Purpose |
|---|---|
| `log_parser.py` | The main script |
| `sample.log` | A small example log for testing |
| `summary.txt` | Created only if you use `--out` |
| `README.md` | This file |

## What I learned

- How to read a file line by line without loading it all into memory
- How to use a regular expression to find patterns in text
- How `Counter` makes counting things very easy
- How to build a command-line tool with `argparse`
- How to handle file errors properly instead of letting the script crash

## Ideas for later

- Filter by date or time range
- Read several log files at once
- Run it every day with cron and send the summary by email
