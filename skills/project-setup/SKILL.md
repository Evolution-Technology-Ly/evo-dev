---
name: project-setup
description: "Prepare or refresh concise repository instructions and task continuity. Use when explicitly invoked to onboard a repository or a named area; ordinary development does not require rerunning setup."
---

# Evo Project Setup

Prepare the smallest useful repository guidance from observed evidence. This is the reusable onboarding workflow in evo-dev, by Evolution Technology. Adapt to the repository; do not import another project's architecture or business rules.

## Establish scope and preserve work

- Use the current repository or the area explicitly named by the user. Identify its Git root, branch, HEAD, and staged, unstaged, and untracked work before editing. In a folder containing multiple repositories, scope the work to the intended repository; clarify an ambiguous target before writing.
- Read applicable global and scoped instructions, relevant existing guidance (including CLAUDE.md when present), and any checkpoint for the active task. Preserve useful rules and accepted decisions. Do not replace existing guidance wholesale or overwrite concurrent edits; reread target files immediately before editing and reconcile their current contents.
- Limit setup changes to relevant instructions, task state, and links needed to find them. Preserve application code, tests, dependencies, configuration, user files, and the index. Leave staging, commits, pushes, resets, branch changes, and history to the user.
- Treat legacy setup removal as a separate scope unless explicitly requested. Identify unnecessary files or integrations without deleting them, installing replacements, or changing global settings.

## Learn only what changes future decisions

Inspect the affected implementation, a representative test when available, build/package manifests, relevant CI commands, and existing decision documents. Follow links selectively; do not inventory the whole codebase or generate an architecture encyclopedia.

Distinguish observed implementation, explicit accepted decisions, and historical or proposed designs. Correct stale factual guidance only with evidence; surface material contradictions. Ask about intent that cannot be established while continuing independent inspection. For a new or empty repository, use known user decisions and available files; leave unknown architecture, conventions, and commands unstated rather than inventing them.

## Create or improve the applicable AGENTS.md

Reuse the existing instruction structure. Create a root AGENTS.md when repository-wide guidance is needed; for a scoped area, use or update the nearest applicable file and avoid unrelated areas. Preserve intentional overrides and routing to existing guidance.

Include only information that materially helps future work:

- Non-obvious boundaries, domain invariants, accepted decisions, and recurring corrections supported by evidence.
- Links to representative implementations or decision documents where they save expensive rediscovery. State when to read them.
- Relevant existing build, analyzer, and test commands, relative to an identified working directory, with meaningful prerequisites and the actual CI coverage.
- A link to the active task's checkpoint when one is warranted.

Keep guidance concise. Prefer executable checks for mechanically enforceable rules. Link to maintained detail rather than duplicating it or restating global preferences. Avoid machine-specific paths, redundant CLAUDE.md copies, speculative rules, and summaries readily discoverable from source. Repeated setup should make focused corrections; leave already adequate guidance unchanged.

## Preserve task continuity only when useful

Use a checkpoint when a known active task spans sessions, needs a handoff, or has meaningful unfinished work and decisions expensive to reconstruct. Setup alone does not warrant a checkpoint. Reuse one checkpoint owned by that task; do not create a competing file or combine unrelated concurrent tasks.

Follow the repository's existing location and format. Otherwise use a short, descriptive path such as docs/<task>-checkpoint.md. Record the objective and boundaries, branch/HEAD and relevant working-tree state, accepted decisions and evidence links, completed versus remaining work, dated verification and its limits, blockers, and the next concrete step. Record only established facts; commit subjects and old test results do not prove current completion or coverage.

On resume, reconcile the checkpoint with current Git and user instructions. After compaction, use it to recover missing task state and reread applicable instructions when their scope or contents are uncertain. Update current state at meaningful handoffs instead of appending an action log. Preserve other task owners' state.

## Verify and report

Check edited links, command provenance, instruction scope, the final diff, and preservation of pre-existing work. Documentation-only setup does not require running the application or a full test suite. Do not start services, reset databases, or install tools merely to validate onboarding.

Report the files changed and why, checks actually performed, material unresolved questions, and how to start the next task or resume its checkpoint. Distinguish inspected commands from commands executed. If existing guidance already suffices, say so without creating extra files.
