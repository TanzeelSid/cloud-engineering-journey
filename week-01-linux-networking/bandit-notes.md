# Bandit Notes — Levels 0 to 15 (OverTheWire)

Bandit is a beginner Linux wargame: each level is a small puzzle, and solving it reveals the password for the *next* level. This note walks through Levels 0 → 15 in plain English, with the exact commands used and the resulting password for each step.

---

## Level 0 — Getting In

**Goal:** just connect. Username and password for level 0 are publicly given by the game itself (`bandit0` / `bandit0`) — not a puzzle yet, just practice using SSH.

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

---

## Level 0 → 1

**Goal:** the password for bandit1 is sitting in a file called `readme` in the home directory.

```bash
ls
cat readme
```

**Password for bandit1:** `6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR`

---

## Level 1 → 2

**Goal:** the password is in a file literally named `-` (a single dash). `cat -` alone doesn't work — `cat` treats a bare `-` as "read from keyboard input," not as a filename. Fix: point at it with a path so it's unambiguous.

```bash
ls
cat ./-
```

**Password for bandit2:** `PK8fYLZg2hnHSz83plBL1iEPKdD3QToB`

---

## Level 2 → 3

**Goal:** the password is in a file named `spaces in this filename` — actual spaces in the name. `cat` alone will treat that as several different filenames. Fix: wrap it in quotes.

```bash
ls
cat "spaces in this filename"
```

**Password for bandit3:** `7ZZ2LFrykP2zEyvBl4m3clcL7tGYJPME`

---

## Level 3 → 4

**Goal:** password is inside a folder called `inhere`, but it's a *hidden* file (name starts with a dot, so plain `ls` won't show it).

```bash
cd inhere
ls -la
cat .hidden
```

**Password for bandit4:** `xzTXq1rDJQVVAzdv5cHq1TQytTWufAMq`

---

## Level 4 → 5

**Goal:** `inhere` has several files with junk names, but only ONE is actual human-readable text — the rest are garbage/binary. `file` tells you what type each one really is.

```bash
cd inhere
file ./*
cat ./-file07
```

(the exact filename that comes back as "ASCII text" may differ each time you play — use whichever one `file` flags as text)

**Password for bandit5:** `6C7h9GD8M6ai5nr7wo1RonrzFjj9yIrG`

---

## Level 5 → 6

**Goal:** somewhere inside `inhere` (which now has nested subfolders) is one file matching: human-readable, exactly 1033 bytes, not executable. `find` can filter by exact size.

```bash
cd inhere
find . -size 1033c
cat ./<path-that-find-returned>
```

**Password for bandit6:** `pXa26xhMWaC2SvDotA4r9EgZkulOeSBW`

---

## Level 6 → 7

**Goal:** the password file is no longer in your home directory — it's somewhere on the *entire* filesystem. You're told three facts about it: owned by user `bandit7`, group `bandit6`, and exactly 33 bytes. `find` can search from the root (`/`) using all three as filters. `2>/dev/null` hides the wall of "permission denied" noise from folders you can't read.

```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
```

**Password for bandit7:** `Bmnnvf82KzQlfxgAl2d1zYbr1u9pr3E3`

---

## Level 7 → 8

**Goal:** a big file `data.txt` contains many words, and the password sits right next to the word `millionth`. `grep` searches for a pattern and prints the matching line(s).

```bash
grep millionth data.txt
```

**Password for bandit8:** `VR1ljMayciFxbnUokuQmJFw6QC9VKtub`

---

## Level 8 → 9

**Goal:** `data.txt` has thousands of duplicate lines — except the password line, which appears exactly once. `sort` groups identical lines together, then `uniq -u` prints only the lines that appear *once*.

```bash
sort data.txt | uniq -u
```

**Password for bandit9:** `EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl`

---

## Level 9 → 10

**Goal:** `data.txt` is mostly binary junk with the password buried inside it. `cat` would just spam your terminal with garbage. `strings` pulls out only the readable text chunks; the real hint text says the password is preceded by several `=` characters, so filter for that.

```bash
strings data.txt | grep =
```

**Password for bandit10:** `B0s2khmbT9u0geKuOoVGW3JZKhndE3BG`

---

## Level 10 → 11

**Goal:** the password in `data.txt` is Base64-encoded (that jumbled text ending in `=` signs you sometimes see). `base64 --decode` reverses it.

```bash
cat data.txt | base64 --decode
```

**Password for bandit11:** `pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro`

---

## Level 11 → 12

**Goal:** the text in `data.txt` has been run through ROT13 — every letter shifted 13 places in the alphabet (so A↔N, B↔O, etc.). `tr` (translate characters) can undo it in one line.

```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

**Password for bandit12:** `GROozWPO8QyN0mGrjUkID0WCYkZiQxrN`

---

## Level 12 → 13

**Goal:** the hardest one so far. `data.txt` is a **hex dump** of a file that's been compressed *multiple times in a row* (gzip, then bzip2, then gzip, then tar, etc., stacked). The process: convert the hex dump back to real binary, then repeatedly check the file type and decompress, one layer at a time, until you land on plain text.

```bash
mkdir /tmp/mywork
cp data.txt /tmp/mywork
cd /tmp/mywork

xxd -r data.txt data1        # undo the hex dump → real compressed file
file data1                   # check what it actually is

# Then repeat this pattern for however many layers file reveals — could be gzip, bzip2, tar, or others:
mv data1 data2.gz && gzip -d data2.gz && file data2
mv data2 data3.bz2 && bzip2 -d data3.bz2 && file data3
mv data3 data4.gz && gzip -d data4.gz && file data4
tar -xvf data4 && file data5.bin
mv data5.bin data6.gz && gzip -d data6.gz && file data6
# ...keep checking `file` after each step and matching the extension to what it reports,
# until `file` finally says "ASCII text" — then:
cat <final-file>
```

**Why it's written as "repeat the pattern" instead of one fixed sequence:** the exact chain of compression types is randomized per playthrough, so the number of layers and their order can differ. Run `file` after every decompression step and let it tell you what to do next.

**Password for bandit13:** `qQYQiHOBPR8zR61qxYqX45quvihF2uzk`

---

## Level 13 → 14

**Goal:** no password this time — you're handed an SSH **private key** (`sshkey.private`) and use it to log in directly as bandit14, no password needed.

```bash
ls
ssh bandit14@bandit.labs.overthewire.org -p 2220 -i private.key
```

---

## Level 14 → 15

**Goal:** as bandit14, your own password is sitting in a root-only-readable file — read it, then "submit" it to a listening service on port 30000 on localhost, which checks it and hands back the next password.

```bash
cat /etc/bandit_pass/bandit14
nc localhost 30000
# paste the password you just read, press Enter
```

(`telnet localhost 30000` works the same way if `nc`/netcat isn't available.)

**Password for bandit15:** `aaWecNkG4FhxJQxz07uiwzVP6bJiYS65`

---

## Level 15 → 16

**Goal:** same idea as Level 14, but this time the service on port 30001 expects an **encrypted (SSL/TLS)** connection, not plain text — so plain `nc` won't work. `openssl s_client` speaks SSL/TLS and can hold the connection open with `-ign_eof`.

```bash
cat /etc/bandit_pass/bandit15
openssl s_client -connect localhost:30001 -ign_eof
# paste the password you just read, press Enter
```

**Password for bandit16:** `pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7`

---

## Quick Reference — Password Table

| Unlocks login as | Password |
|---|---|
| bandit1 | `6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR` |
| bandit2 | `PK8fYLZg2hnHSz83plBL1iEPKdD3QToB` |
| bandit3 | `7ZZ2LFrykP2zEyvBl4m3clcL7tGYJPME` |
| bandit4 | `xzTXq1rDJQVVAzdv5cHq1TQytTWufAMq` |
| bandit5 | `6C7h9GD8M6ai5nr7wo1RonrzFjj9yIrG` |
| bandit6 | `pXa26xhMWaC2SvDotA4r9EgZkulOeSBW` |
| bandit7 | `Bmnnvf82KzQlfxgAl2d1zYbr1u9pr3E3` |
| bandit8 | `VR1ljMayciFxbnUokuQmJFw6QC9VKtub` |
| bandit9 | `EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl` |
| bandit10 | `B0s2khmbT9u0geKuOoVGW3JZKhndE3BG` |
| bandit11 | `pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro` |
| bandit12 | `GROozWPO8QyN0mGrjUkID0WCYkZiQxrN` |
| bandit13 | `qQYQiHOBPR8zR61qxYqX45quvihF2uzk` |
| bandit14 | *(no password — SSH key login)* |
| bandit15 | `aaWecNkG4FhxJQxz07uiwzVP6bJiYS65` |
| bandit16 | `pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7` |

## Core Commands Used, In One Place

| Command | Job |
|---|---|
| `ls -la` | show all files, including hidden ones |
| `cat ./-`, `cat "name with spaces"` | read a file with a tricky name |
| `file ./*` | figure out what type each file actually is |
| `find . -size 1033c` | find a file by exact byte size |
| `find / -user X -group Y -size Nc 2>/dev/null` | find a file anywhere by owner/group/size |
| `grep word file` | find a line containing a word |
| `sort file \| uniq -u` | find the one line that isn't duplicated |
| `strings file \| grep pattern` | pull readable text out of binary junk |
| `base64 --decode` | undo Base64 encoding |
| `tr 'A-Za-z' 'N-ZA-Mn-za-m'` | undo ROT13 |
| `xxd -r` | undo a hex dump back to binary |
| `gzip -d` / `bzip2 -d` / `tar -xvf` | undo each layer of compression |
| `ssh -i keyfile user@host` | log in using a private key instead of a password |
| `nc host port` | send text to a listening network service |
| `openssl s_client -connect host:port` | same idea as `nc`, but encrypted |
