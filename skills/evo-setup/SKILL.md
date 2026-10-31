---
name: evo-setup
description: "Apply the bundled evo-dev personal preferences after installing the plugin. Run only when explicitly invoked for plugin onboarding or a deliberate profile refresh."
---

# Evo Dev Setup

Apply the bundled personal development profile to this machine without changing existing settings or installing duplicate skills. This is explicit onboarding, not an installation hook.

Resolve resources from this installed SKILL.md, not the user's working directory. The plugin root is two directories above this skill directory. Read [the profile](../../profile/AGENTS.md) and the matching installer before running it. Use the installed package; do not clone a repository or download another setup script.

Run the installer with **profile-only mode**:

- Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File "<plugin-root>\setup.ps1" -ProfileOnly` (or `pwsh` when appropriate).
- macOS/Linux: `sh "<plugin-root>/setup.sh" --profile-only`.

Use an absolute path to the installed script. Do not pass the default full-install mode: Codex already manages the plugin's skills. Respect CODEX_HOME when configured; otherwise the destination is the user's ~/.codex/AGENTS.md. Do not change model settings, credentials, plugins, repositories, or checkpoints.

The installer copies only a missing profile and leaves existing identical content unchanged. For REVIEW output or a failure, inspect the reported condition; preserve the existing content and report what needs reconciliation. Do not silently overwrite, append a second instruction set, remove an override, or delete another skill installation. Make a deliberate merge only if the user separately requests it.

Check whether standalone copies of project-setup already exist under ~/.agents/skills or the Codex home skills directory. If so, report the potential duplicate and recommend keeping one installation method after reviewing local customizations. Leave those copies intact.

Report the actual command, exit result, profile destination, and any unresolved differences. After successful setup, tell the user to start a new Codex chat so it loads the profile, open the intended project, and explicitly select the bundled project-setup skill. The host may qualify bundled skill names with the plugin name; use the skill picker when needed. Setup does not modify project guidance until that skill is invoked.
