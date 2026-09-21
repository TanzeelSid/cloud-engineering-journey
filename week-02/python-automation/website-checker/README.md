# Website Up/Down Checker

A small Python script that checks if websites are working. It reads a list of URLs from a text file, visits each one, and tells you if it is **UP** or **DOWN**. At the end it shows an uptime percentage for every site.

This is the same basic idea that cloud monitoring tools use: keep asking "is my service alive?" and raise an alert when the answer is no.

## What it does

- Reads website URLs from a file (`urls.txt`)
- Sends a request to each website using the `requests` library
- Prints the result: UP or DOWN, the HTTP status code, and the response time in milliseconds
- Repeats the checks for a number of rounds, waiting between rounds
- Saves every result to a log file (`checker.log`)
- Prints an uptime summary at the end (for example: 2 out of 2 checks up = 100%)
- Exits with code `1` if any site was down, so other scripts (like Bash) can react to it

## Requirements

- Python 3
- The `requests` library

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

## How to use it

1. Put your URLs in `urls.txt`, one per line. Lines starting with `#` are ignored:

```
# one URL per line
https://www.google.com
https://github.com
https://httpbin.org/status/500
https://this-domain-does-not-exist-12345.com
```

2. Run the script:

```bash
python website_checker.py
```

3. Or run it with your own options:

```bash
python website_checker.py --rounds 2 --interval 3
```

## Options

| Option | Default | What it does |
|---|---|---|
| `--file` | `urls.txt` | The file that contains the URLs |
| `--rounds` | `3` | How many times to check every URL |
| `--interval` | `5` | Seconds to wait between rounds |
| `--log` | `checker.log` | The file where results are saved |

## Example output

```
[2026-09-20 10:15:02] UP   https://www.google.com (HTTP 200, 143ms)
[2026-09-20 10:15:03] UP   https://github.com (HTTP 200, 310ms)
[2026-09-20 10:15:04] DOWN https://httpbin.org/status/500 (HTTP 500, 620ms)
[2026-09-20 10:15:04] DOWN https://this-domain-does-not-exist-12345.com (connection failed)
[2026-09-20 10:15:07] UP   https://www.google.com (HTTP 200, 121ms)
[2026-09-20 10:15:07] UP   https://github.com (HTTP 200, 287ms)
[2026-09-20 10:15:08] DOWN https://httpbin.org/status/500 (HTTP 500, 598ms)
[2026-09-20 10:15:08] DOWN https://this-domain-does-not-exist-12345.com (connection failed)

Uptime summary
  100.0%  https://www.google.com  (2/2 checks up)
  100.0%  https://github.com  (2/2 checks up)
    0.0%  https://httpbin.org/status/500  (0/2 checks up)
    0.0%  https://this-domain-does-not-exist-12345.com  (0/2 checks up)
```

Two of the URLs are broken **on purpose**, so I can see how the script behaves when a site is down.

## How it works (step by step)

1. `read_urls()` opens `urls.txt`, skips empty lines and comments, and returns a list of URLs.
2. For every URL, `check_url()` sends a request with a 5 second timeout.
3. A site counts as **UP** if the HTTP status code is below 400 (200 = OK, 301 = redirect). Codes like 404 or 500 count as **DOWN**.
4. The result is printed on the screen and also written to the log file.
5. The script keeps count of how many checks were UP for each URL.
6. At the end, uptime % = (checks that were up ÷ total checks) × 100.

## Error handling

The script does not crash when something goes wrong. It catches these problems:

| Problem | What the script does |
|---|---|
| Website is too slow (over 5 seconds) | Marks it DOWN with the reason `timeout` |
| Domain does not exist or no internet | Marks it DOWN with the reason `connection failed` |
| Any other request error | Marks it DOWN and shows the error message |
| `urls.txt` is missing | Prints a clear error message and exits with code `2` |
| `urls.txt` is empty | Prints "No URLs found" and exits with code `2` |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | All checks were UP |
| `1` | At least one check was DOWN |
| `2` | Bad input (URL file missing or empty) |

You can use this in Bash:

```bash
python website_checker.py --rounds 1
echo "exit code: $?"
```

## Files in this folder

| File | Purpose |
|---|---|
| `website_checker.py` | The main script |
| `urls.txt` | The list of websites to check |
| `checker.log` | Created when you run the script (not committed to Git) |
| `README.md` | This file |

## What I learned

- How to read a file safely using `with open(...)`
- How to send HTTP requests with `requests` and always set a `timeout`
- How to use `try/except` so one broken website does not stop the whole script
- How exit codes let other tools know if a script succeeded or failed
- How this simple idea connects to real cloud monitoring

## Ideas for later

- Send an email or Slack message when a site is down
- Run it automatically with a cron job
- Run it inside a Docker container
