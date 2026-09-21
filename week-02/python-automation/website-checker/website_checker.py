#!/usr/bin/env python3
"""Website up/down checker: reads URLs from a file, checks each, prints status + uptime."""
import argparse
import sys
import time
from datetime import datetime

import requests


def read_urls(path):
    try:
        with open(path, encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")]
    except FileNotFoundError:
        print(f"Error: URL file '{path}' not found")
        sys.exit(2)


def check_url(url, timeout=5):
    start = time.time()
    try:
        resp = requests.get(url, timeout=timeout)
        ms = round((time.time() - start) * 1000)
        return resp.ok, resp.status_code, ms, ""
    except requests.exceptions.Timeout:
        return False, None, None, "timeout"
    except requests.exceptions.ConnectionError:
        return False, None, None, "connection failed"
    except requests.exceptions.RequestException as e:
        return False, None, None, str(e)


def main():
    p = argparse.ArgumentParser(description="Website up/down checker")
    p.add_argument("--file", default="urls.txt")
    p.add_argument("--rounds", type=int, default=3)
    p.add_argument("--interval", type=int, default=5, help="seconds between rounds")
    p.add_argument("--log", default="checker.log")
    args = p.parse_args()

    urls = read_urls(args.file)
    if not urls:
        print("No URLs found")
        sys.exit(2)

    stats = {u: {"up": 0, "total": 0} for u in urls}

    with open(args.log, "a", encoding="utf-8") as log:
        for rnd in range(1, args.rounds + 1):
            for url in urls:
                is_up, code, ms, err = check_url(url)
                stats[url]["total"] += 1
                stats[url]["up"] += is_up
                stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                detail = f"HTTP {code}, {ms}ms" if code else err
                line = f"[{stamp}] {'UP  ' if is_up else 'DOWN'} {url} ({detail})"
                print(line)
                log.write(line + "\n")
            if rnd < args.rounds:
                time.sleep(args.interval)

    print("\nUptime summary")
    any_down = False
    for url, s in stats.items():
        pct = s["up"] / s["total"] * 100
        any_down |= s["up"] < s["total"]
        print(f"  {pct:5.1f}%  {url}  ({s['up']}/{s['total']} checks up)")
    sys.exit(1 if any_down else 0)


if __name__ == "__main__":
    main()
