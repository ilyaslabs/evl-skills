---
description: Map this whole project with EVL flows, branches and resources
argument-hint: "[optional notes, e.g. skip the legacy module]"
---
Use the evl-flows skill to map this project with EVL. $ARGUMENTS

1. Add the `io.github.ilyaslabs:evl-annotations` dependency (version from the skill) to every module you tag.
2. Find every entry point: HTTP endpoints, scheduled jobs, queue consumers, CLI commands. Give each a root `@Flow` with a clear label and description.
3. Tag the meaningful steps under each flow in call order (`@Flow` on methods, `// @flow` markers inline). Skip getters, mappers and plumbing.
4. Declare branches with `x?` decision segments plus `when`, loops with `each`, error paths with `onError`. Tag only what the code really does; never invent branches.
5. Shared code: tag it in every flow where it is a meaningful step (comma-separated paths on the marker).
6. Mark databases, queues, caches, storage, external APIs and jobs with the matching `@EVL.*` annotation.
7. Work module by module. After each module run the evl CLI and fix every warning.

Finish with the flow tree and a short summary of the flows you created.
