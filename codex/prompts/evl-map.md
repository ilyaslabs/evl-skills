---
description: Map one module or folder with EVL flows
argument-hint: "<module or folder>"
---
Use the evl-flows skill to map only `$ARGUMENTS` with EVL. If no module is given, ask which one.

1. Add the `io.github.ilyaslabs:evl-annotations` dependency to this module if it is missing.
2. Give every entry point in it a root `@Flow` with a label and description, then tag its meaningful steps in call order.
3. Declare branches (`x?` + `when`), loops (`each`) and error paths (`onError`) only where the code really has them.
4. Reuse existing flow paths from other modules when this code is a step in them; do not create duplicates.
5. Mark databases, queues, caches, storage, external APIs and jobs with `@EVL.*`.
6. Run the evl CLI on the module, fix every warning, and show its flow tree.

Do not change code outside `$ARGUMENTS`.
