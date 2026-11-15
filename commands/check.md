---
description: Check EVL tags with the CLI, fix warnings, show the flow tree
argument-hint: "[folder]"
---
Use the evl-flows skill to check the EVL tags in `$ARGUMENTS (or the project root if empty)`.

1. Run the evl CLI on it.
2. Fix every warning and error (duplicate or broken paths, unknown resources, steps without a root). Do not add new flows.
3. Run the CLI again and show the final flow tree with a one-line note per fix.
