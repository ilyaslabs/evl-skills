---
description: Update EVL tags for the code you changed (git diff)
argument-hint: "[base branch, default: uncommitted changes]"
---
Use the evl-flows skill to keep the EVL map in sync with recent changes.

1. Look at the changes: `git diff $ARGUMENTS` if a base is given, otherwise uncommitted changes (`git diff HEAD`).
2. For each changed method or class: add tags for new meaningful steps, move or rename paths that changed, remove tags from deleted steps, and update `when` / `each` / `onError` if the logic changed.
3. Touch only tags related to the diff.
4. Run the evl CLI, fix warnings, and list what you added, changed and removed.
