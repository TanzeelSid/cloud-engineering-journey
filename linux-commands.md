# Linux Command Cheat Sheet — Week 1 (Cloud Engineering Journey)

Personal quick-reference built during Week 1 (Linux fundamentals + networking basics) of my Cloud Engineering / DevOps roadmap. Focused on Ubuntu, and on commands I'll actually reach for in cloud/DevOps work — not an exhaustive Linux manual.

## Corrections & Additions Log

**Corrected from my original notes:**
- `rm -rf` — my notes said "use with caution" but didn't explain *why*. It deletes recursively, skips confirmation, and there's no trash/undo. Added a real warning + safer alternative below.
- `kill -9 <PID>` — jumping straight to `-9` was listed with no warning. `-9` (SIGKILL) doesn't let the process clean up or save data. Correct order is `kill <PID>` first, `-9` only if it won't die.
- `netstat -tuln` — `netstat` is deprecated and often not installed by default on modern Ubuntu. `ss -tuln` is the current standard; kept as the primary command.
- `chmod 755` — original note gave the command but not what the numbers mean. Explained the octal permission model below so it's not memorized blindly.
- `tail -f` — correct as written; clarified it's a *live* follow, distinct from a one-time `tail -n`.

**Added (missing but genuinely useful for Cloud/DevOps work):**
- Sections 2 (touch), 4 (diff), 6 (jobs/bg/fg/nohup), 10 (Users & Groups), 11 (Environment Variables & Shell), 13 (SSH & Remote File Transfer), 14 (Archives & Compression), 15 (System Info), 16 (Help & Documentation) — none of these existed in my original notes.
- `find`, `ssh-keygen`, `tar`, `man`/`--help`, `sudo adduser`/`usermod`, `curl`/`wget`, `uname -a` — commonly needed for server work and troubleshooting.

---

## 1. Navigation & File Management

### `pwd`
**Purpose:** Print the current working directory.
```bash
pwd
```
**Useful when:** Confirming which directory you're in before running a destructive command.

### `ls`, `ls -l`, `ls -la`, `ls -lh`
**Purpose:** List directory contents.
```bash
ls        # names only
ls -l     # long format: permissions, owner, size, date
ls -la    # long format + hidden files (dotfiles)
ls -lh    # long format with human-readable sizes (KB/MB/GB)
```
**Useful when:** Checking file permissions, hidden config files, or file sizes.

### `cd`
**Purpose:** Change directory.
```bash
cd /path/to/dir
cd ..      # up one level
cd ~       # home directory
cd -       # previous directory
```

### `cp`, `mv`, `rm`, `rmdir`
**Purpose:** Copy, move/rename, and delete files or directories.
```bash
cp source dest         # copy a file
cp -r sourcedir dest    # copy a directory (recursive)
mv old new              # move or rename
rm filename             # delete a file
rmdir dirname           # delete an EMPTY directory only
rm -r dirname           # delete a directory and its contents
```
**⚠️ `rm -rf`** — see [Safety / Common Mistakes](#17-safety--common-mistakes) before using this.

### `mkdir -p`
**Purpose:** Create directories, including any missing parent folders.
```bash
mkdir -p path/to/dir
```
**Useful when:** Creating a nested folder structure in one command instead of one level at a time.

### `find` 🆕
**Purpose:** Search for files/directories by name, type, or other attributes.
```bash
find . -name "*.log"              # find by filename pattern, from current dir
find /var/log -type f -mtime -1   # files modified in the last day
```
**Useful when:** Locating config files or logs scattered across a filesystem.

---

## 2. File Creation, Editing & Viewing

### `touch` 🆕
**Purpose:** Create an empty file (or update its timestamp if it exists).
```bash
touch notes.txt
```

### `nano` / `vim`
**Purpose:** Interactive text editors.
```bash
nano filename   # simple, beginner-friendly
vim filename    # powerful, steeper learning curve
```
**Useful when:** `nano` for quick edits; `vim` once you're comfortable, since it's preinstalled almost everywhere (including minimal servers).

### `cat`, `less`
**Purpose:** View file contents.
```bash
cat filename    # dump entire file to screen
less filename   # scroll through a file page by page (q to quit)
```
**Useful when:** `cat` for short files, `less` for anything long (logs, configs).

### `head`, `tail`, `tail -f`
**Purpose:** View the start or end of a file.
```bash
head -n 20 file   # first 20 lines
tail -n 20 file   # last 20 lines
tail -f file      # live-follow a growing file (Ctrl+C to stop)
```
**Useful when:** `tail -f` is the standard way to watch a log file in real time.

---

## 3. Permissions & Ownership

### `chmod`
**Purpose:** Change file/directory permissions.
```bash
chmod 755 filename   # owner: rwx, group: r-x, others: r-x
chmod +x script.sh   # add execute permission
chmod -R 755 dir/    # apply recursively to a directory
```
**Permission model:** each digit = read(4) + write(2) + execute(1), for **owner / group / others**. `755` = owner has 7 (rwx), group and others have 5 (r-x).
**Useful when:** Making a script executable, or fixing "permission denied" errors.

### `chown`
**Purpose:** Change file/directory ownership.
```bash
chown user:group filename
chown -R user:group dir/   # recursive
```
**⚠️** See safety notes — recursive `chown`/`chmod` on the wrong path can break a system.

---

## 4. Text Processing & Searching

### `grep`
**Purpose:** Search text for a pattern.
```bash
grep "pattern" filename
grep -i "pattern" filename    # case-insensitive
grep -r "pattern" directory/  # recursive, search a whole folder
grep -n "pattern" filename    # show line numbers
```
**Useful when:** Finding an error string across log files.

### `cut`, `awk`
**Purpose:** Extract columns/fields from text.
```bash
cut -d',' -f1 file.csv        # first field, comma-delimited
awk '{print $1}' file         # first whitespace-delimited field
```

### `sort`, `uniq`
**Purpose:** Sort lines and remove/report duplicates.
```bash
sort file
uniq -u file          # print only unique (non-duplicate) lines
sort file | uniq -c   # common combo: count occurrences of each line
```

### `wc`
**Purpose:** Count lines, words, characters.
```bash
wc -l file   # line count
wc -w file   # word count
```

### `diff` 🆕
**Purpose:** Compare two files line by line.
```bash
diff file1 file2
```
**Useful when:** Checking what changed between two config versions before overwriting one.

---

## 5. Pipes & Redirection

### Pipe `|`
**Purpose:** Send the output of one command as input to the next.
```bash
ps aux | grep nginx
```

### Redirection `>`, `>>`
**Purpose:** Send command output to a file.
```bash
command > file    # overwrite file
command >> file   # append to file
```
**⚠️** `>` silently overwrites — double-check the filename before running it.

---

## 6. Processes & Jobs

### `ps aux`, `top` / `htop`
**Purpose:** View running processes.
```bash
ps aux    # snapshot of all processes
top       # live, refreshing view (built-in)
htop      # nicer live view (install: sudo apt install htop)
```

### `kill`, `kill -9`
**Purpose:** Stop a process by PID.
```bash
kill <PID>       # SIGTERM — ask the process to shut down cleanly
kill -9 <PID>    # SIGKILL — force-kill immediately, no cleanup
```
**⚠️** Always try plain `kill` first. Reach for `-9` only if the process ignores the polite request.

### `jobs`, `bg`, `fg`, `nohup` 🆕
**Purpose:** Manage processes running in your current shell session.
```bash
long-command &        # run in background
jobs                   # list background jobs in this shell
fg %1                  # bring job 1 to foreground
nohup long-command &   # keep running even after you log out
```

---

## 7. Services & Logs

### `systemctl`
**Purpose:** Manage system services (systemd).
```bash
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl status nginx
sudo systemctl enable nginx   # auto-start on boot
```

### `journalctl`
**Purpose:** View systemd service logs.
```bash
journalctl -u nginx   # logs for one service
journalctl -f          # live-follow all logs
journalctl -xe         # recent logs with extra context (good after a crash)
```

---

## 8. Package Management — Ubuntu/Debian

```bash
sudo apt update              # refresh package index (do this first)
sudo apt upgrade             # upgrade installed packages
sudo apt install <package>   # install
sudo apt remove <package>    # uninstall
apt list --installed         # list installed packages
dpkg -l                      # lower-level package list
```
**Note:** other distros use different tools (`yum`/`dnf` on RHEL/Fedora, `pacman` on Arch) — not needed for this roadmap, just be aware they exist.

---

## 9. Disk & System Health

```bash
df -h          # disk space per filesystem, human-readable
du -sh /path   # total size of a directory
free -h        # memory usage
uptime         # how long the system's been running + load average
```

---

## 10. Users & Groups 🆕

```bash
whoami                             # current username
id                                 # current user's UID/GID and group memberships
sudo adduser newuser               # create a user (Ubuntu-friendly wrapper)
sudo usermod -aG groupname user    # add a user to a group
groups username                    # list a user's groups
```

---

## 11. Environment Variables & Shell 🆕

```bash
echo $PATH             # show directories the shell searches for commands
export VAR=value       # set an environment variable for this session
alias ll='ls -la'      # create a shortcut command
history                # show recent command history
source ~/.bashrc       # reload shell config without restarting the terminal
```

---

## 12. Networking & Troubleshooting

```bash
ip a                            # show IP addresses / network interfaces
ping -c 4 8.8.8.8                # test connectivity (4 pings, then stop)
ss -tuln                         # list open ports/sockets (current standard; netstat is deprecated)
curl https://example.com         # fetch a URL, print response
wget https://example.com/file    # download a file
```
**Useful when:** `ping` checks basic reachability, `ss` checks what's listening locally, `curl`/`wget` test/fetch over HTTP.

---

## 13. SSH & Remote File Transfer 🆕

```bash
ssh user@remote_host                          # log into a remote machine
ssh-keygen -t ed25519 -C "you@example.com"    # generate an SSH key pair
scp file.txt user@host:/path/                 # copy a file TO a remote host
scp -r dir/ user@host:/path/                  # copy a directory (recursive)
scp user@host:/path/file.txt .                # copy a file FROM a remote host
```

---

## 14. Archives & Compression 🆕

```bash
tar -czvf archive.tar.gz folder/   # create a compressed archive
tar -xzvf archive.tar.gz           # extract one
```
(`c`=create, `x`=extract, `z`=gzip, `v`=verbose, `f`=filename)

---

## 15. Useful System Information 🆕

```bash
uname -a          # kernel and system info
lsb_release -a    # Ubuntu version info
hostname          # machine's network name
```

---

## 16. Command Help & Documentation 🆕

```bash
man command      # full manual page (q to quit)
command --help   # quick usage summary
which command    # show which executable would run
type command     # show if it's a builtin, alias, or binary
```

---

## 17. Safety / Common Mistakes

| Command | Risk | Safer approach |
|---|---|---|
| `rm -rf` | Deletes recursively, no confirmation, no undo | `ls` the target first; consider `rm -ri` (asks per file) or `trash-cli` |
| `sudo` (any command) | Runs with full root privileges — a mistake here can affect the whole system | Read the full command before running; never blindly copy-paste `sudo` commands from the internet |
| `chmod`/`chown -R` (wrong path or `777`) | Can break permissions system-wide or expose files to everyone | Use the narrowest permission that works; double-check the target path |
| `kill -9` | No graceful shutdown, possible data loss for the killed process | Try plain `kill` first |
| `curl \| bash` / `wget -O- \| sh` | Runs a downloaded script immediately, unreviewed | Download first, read the script, then run it |

## Quick Safety Rules

- Never run `sudo` or `rm -rf` on autopilot — read the exact command before hitting enter.
- Prefer `rm -r` over `rm -rf` unless you're certain there's nothing to confirm.
- Try `kill` before `kill -9`.
- Test destructive commands on a throwaway file/folder first if unsure.
- When in doubt, `man <command>` or `<command> --help` before running something new.
