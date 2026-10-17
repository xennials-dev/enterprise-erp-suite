---
name: git-upstream-sync
description: >-
  Proactively activates whenever the user or agent needs to synchronize, update,
  fetch, pull, merge, or rebase a local git repository or fork with its upstream source.
  Guarantees zero data loss by strictly stashing uncommitted and untracked changes first,
  verifying remotes, merging cleanly without force flags, pushing to origin, and safely
  restoring stashed work with conflict-insulation guards.
---

# Git Upstream Sync Workflow Agent

This skill provides an automated, failsafe runbook for synchronizing any local repository with its upstream remote while completely safeguarding local uncommitted work.

## Core Directives

1. **Mandatory Pre-Flight Check**: Never run `git merge` or `git pull` if `git status --porcelain -u` returns any uncommitted or untracked changes.
2. **Preservation First**: Always create an identifiable backup stash including untracked files (`git stash push -u -m "pre-sync-backup-..."`).
3. **Strict Zero-Force Rule**: Never invoke `--force`, `-f`, `--hard`, or destructive resets during sync.
4. **Conflict Insulation**: If merge conflicts occur between local and upstream commits, halt immediately and preserve the stash. Do **NOT** pop the stash on top of unresolved conflict markers.

---

## Autonomous Execution Workflow

### Step 1: Pre-Flight & Change Preservation
Inspect the current working tree:
```bash
git status --porcelain -u
```
- If output is non-empty, stash all changes (including untracked):
  ```bash
  git stash push -u -m "pre-sync-backup-$(date +%Y%m%d%H%M%S)"
  ```
- Store the knowledge of whether a stash was created (do not pop later if working tree was already clean).

### Step 2: Remote Configuration Verification
Check existing remotes:
```bash
git remote -v
```
- If `upstream` is missing, configure it:
  ```bash
  git remote add upstream <UPSTREAM_URL>
  ```
- If `upstream` exists with a different target URL:
  ```bash
  git remote set-url upstream <UPSTREAM_URL>
  ```

### Step 3: Fetch & Clean Merge
Ensure the active branch is the intended target (e.g. `main`):
```bash
git checkout main
git fetch upstream main
git merge upstream/main -m "chore: merge upstream/main into main"
```
- **If Merge Succeeds**: Proceed to Step 4.
- **If Merge Conflicts Occur**: Stop immediately. Notify the user of conflicting files. Leave the stash untouched.

### Step 4: Propagate to Fork (Origin)
Push the synchronized state up to the fork repository:
```bash
git push origin main
```

### Step 5: Restore Working Tree
If a backup stash was created in Step 1:
```bash
git stash pop
```
- If clean: Synchronization is complete.
- If stashing conflict arises: Alert the user that working tree has conflict markers and the stash remains saved in `git stash list`.

---

## Automated Script Execution
When the repository provides the automated synchronization scripts:
- **Bash**: `./scripts/sync-upstream.sh <UPSTREAM_URL> [BRANCH]`
- **PowerShell**: `.\scripts\sync-upstream.ps1 -UpstreamUrl "<UPSTREAM_URL>" -TargetBranch "main"`
