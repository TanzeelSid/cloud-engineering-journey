#!/usr/bin/env python3
"""Log parser: counts log levels, shows top errors, prints a summary."""
import argparse
import re
import sys
from collections import Counter

LEVEL_RE = re.compile(r"\b(CRITICAL|ERROR|WARN(?:ING)?|INFO|DEBUG)\b")


def parse_log(path):
    levels, errors, total = Counter(), Counter(), 0
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                total += 1
                m = LEVEL_RE.search(line)
                if not m:
                    levels["OTHER"] += 1
                    continue
                level = "WARN" if m.group(1) == "WARNING" else m.group(1)
                levels[level] += 1
                if level in ("ERROR", "CRITICAL"):
                    errors[line[m.end():].strip(" :-")] += 1
    except FileNotFoundError:
        print(f"Error: file '{path}' not found")
        sys.exit(2)
    except PermissionError:
        print(f"Error: no permission to read '{path}'")
        sys.exit(2)
    return total, levels, errors


def build_summary(path, total, levels, errors, top):
    err_count = levels["ERROR"] + levels["CRITICAL"]
    rate = (err_count / total * 100) if total else 0
    out = [f"Log summary: {path}", f"Total lines: {total}"]
    for lvl in ("CRITICAL", "ERROR", "WARN", "INFO", "DEBUG", "OTHER"):
        if levels[lvl]:
            out.append(f"  {lvl:<9}{levels[lvl]}")
    out.append(f"Error rate: {rate:.1f}% ({err_count} error lines)")
    if errors:
        out.append(f"Top {top} errors:")
        for msg, n in errors.most_common(top):
            out.append(f"  {n}x  {msg}")
    return "\n".join(out), err_count


def main():
    p = argparse.ArgumentParser(description="Simple log parser")
    p.add_argument("logfile")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--out", help="also write the summary to this file")
    p.add_argument("--max-errors", type=int, default=None,
                   help="exit 1 if error lines exceed this number")
    a = p.parse_args()

    total, levels, errors = parse_log(a.logfile)
    summary, err_count = build_summary(a.logfile, total, levels, errors, a.top)
    print(summary)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(summary + "\n")
    if a.max_errors is not None and err_count > a.max_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
