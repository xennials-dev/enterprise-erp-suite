# Git Upstream Synchronization & Data Safety Rule

Whenever performing git sync, upstream merge, or repository pulls:
1. **Never perform destructive git commands**: Never use `git push --force`, `git reset --hard`, or `git clean -fd` without explicit user instruction.
2. **Always preserve uncommitted and untracked work first**: Run `git stash push -u -m "pre-sync-backup"` before initiating any branch checkout, merge, rebase, or pull operation.
3. **Always verify remotes before merging**: Ensure `upstream` and `origin` remotes point to the intended targets before fetching.
4. **Insulate merge conflicts**: If conflicts occur during an upstream merge, never pop stashes over conflict markers. Preserve the stash until the tree is clean.
