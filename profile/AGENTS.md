# Personal development preferences

- Inspect the relevant implementation and a representative test before changing code. Follow each repository's architecture, naming, libraries, and conventions; introduce an abstraction or dependency only when the task justifies it.
- Keep changes focused. For refactoring, preserve behavior, public contracts, authorization, persistence, and domain invariants unless the requested scope explicitly changes them.
- Check the current branch and working tree. Preserve existing work, including uncommitted changes. Leave staging, commits, pushes, and history changes to me unless I explicitly request them.
- Use existing build, analyzer, and test commands proportionately. For behavior changes, cover the relevant failure paths as well as success. Report the commands actually run, their results, and any checks that remain unverified.
- Read documentation according to the affected area. Prefer current implementation, executable checks, and explicit accepted decisions over stale summaries; surface material contradictions instead of silently choosing a rule.
- After compaction, recover missing task details from the active checkpoint when needed. When resuming, reconcile it with Git. Reread applicable instructions if their scope or contents are uncertain or may have changed.
- Preserve meaningful decisions and unfinished work in one task-owned checkpoint when work spans sessions. Promote recurring corrections to the narrowest useful instruction, document, or executable check; avoid logging every action.
- Communicate concisely: explain what changed, why, verification, and material remaining uncertainty. Ask about intent that cannot be established from the repository while continuing independent work.
