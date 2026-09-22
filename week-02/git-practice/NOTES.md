# Git Merge Conflict — Practice Notes

## What I did

I created two branches that both changed the same line in `config.txt`:
- `main` set `environment=staging`
- `feature/prod-config` set `environment=production`

When I ran `git merge feature/prod-config` on `main`, Git could not decide
which line to keep, so it stopped and marked the file as conflicted.

## The conflict markers (before resolving)
<<<<<<< HEAD
environment=staging

environment=production

||||||||feature/prod-config

- Between `<<<<<<< HEAD` and `=======` is what my current branch (`main`) had.
- Between `=======` and `>>>>>>> feature/prod-config` is what the other branch had.

## How I resolved it

I opened `config.txt`, deleted all three marker lines, and kept:
environment=production

Then I ran:

```bash
git add config.txt
git commit
```

## Proof of the merge (git log --graph)
*   78e2aa2 (HEAD -> main) Merge branch 'feature/prod-config'
|\  
| * d7ef1a0 (feature/prod-config) Set environment to production
* | 228e691 Set environment to staging
|/  
* f497f96 (origin/main) Teammate edits README
* e1a9be4 Add config

## What I learned

- A merge conflict happens when two branches change the same line.
- `git merge --abort` is a safe way to back out if I panic mid-conflict.
- Conflict markers show both versions side by side; I choose or combine, then delete the markers myself.
- After resolving, the file has to be `git add`-ed before `git commit` will work.
