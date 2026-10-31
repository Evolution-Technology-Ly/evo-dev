# evo-dev

Minimal Codex development configuration for **Evolution Technology**: personal preferences and one explicitly invoked repository onboarding skill, based on the EvoCommerce pilot.

## Install

Install Codex and clone this repository wherever you keep development tools. From the checkout root, run:

**macOS or Linux** (system shell and standard utilities):

```sh
sh ./setup.sh
```

**Windows** (Windows PowerShell 5.1 or PowerShell 7):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

The Windows command permits this script for that process; it does not change your saved execution policy. Organization-enforced policies may still apply. With PowerShell 7 you can use `pwsh -NoProfile -File ./setup.ps1` instead.

Setup installs:

| Source | Destination |
| --- | --- |
| [Personal preferences](profile/AGENTS.md) | `~/.codex/AGENTS.md` |
| [project-setup skill](skills/project-setup/SKILL.md) and its invocation policy | `~/.agents/skills/project-setup/` |

If `CODEX_HOME` is set, preferences go there instead of `~/.codex`. The skill stays in the user's `.agents/skills` directory. Setup requires no administrator access, downloads, Python, Node, or extra services.

Setup copies missing items, skips identical content, and **never overwrites existing differing files or links**. It leaves `config.toml`, credentials, plugins, other skills, repositories, and checkpoints alone. Existing matching links from the original pilot remain intact. Copies on new machines remain usable if you move or delete this checkout.

If setup prints `REVIEW`, it preserves the existing item and exits nonzero. Compare it with the displayed package source and merge manually, then rerun. Some missing items may already have been installed. An existing `AGENTS.override.md` or alternate `CODEX_HOME/skills/project-setup` installation is also reported for review; setup does not remove it or install a duplicate skill.

The same command is safe to rerun. An advanced `--user-directory PATH` shell option or `-UserDirectory PATH` PowerShell parameter targets another user directory, primarily for isolated validation; `CODEX_HOME`, when set, still takes precedence for preferences.

## Work in a repository

Open a new Codex chat in the intended repository and select or send:

```text
$project-setup
```

Optionally add a scope: `$project-setup Focus on the backend.` If the skill is absent from the picker, restart Codex or the IDE extension.

Run the skill once to onboard a repository, or explicitly rerun it to refresh guidance. It inspects current implementation, tests, and existing instructions before creating or improving concise `AGENTS.md` guidance. Useful rules and current work are preserved. A checkpoint is created only for a real continuity need. The skill is explicit-only (`allow_implicit_invocation: false`) and carries no EvoCommerce-specific conventions.

Describe normal development tasks afterward. Repository guidance and task checkpoints stay with their repositories; they are not synchronized through evo-dev. The global profile applies personal defaults across repositories, with scoped project instructions taking precedence as described in the [official instruction documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Skill locations follow the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Update

Edit personal preferences in `profile/AGENTS.md` and reusable onboarding behavior in `skills/project-setup/`. After pulling changes on another machine, rerun setup. Differing installed copies are **reported for manual merging**, not silently updated. Likewise, changes made directly to a machine's global preferences must be reconciled back into this repository deliberately. There is no background synchronization or hidden configuration merge.

The existing pilot skill link follows this checkout's changes automatically; setup retains it when its content matches. New installations use copies consistently on all three platforms.

## Validate

With Python 3 available for development checks:

```sh
python3 -m unittest discover -s tests -v
```

On Windows use `py -3 -m unittest discover -s tests -v`. The checks use temporary user directories and exercise each installer whose shell is available. Unavailable shells are skipped explicitly; passing on one OS does not prove native behavior on the others. Python is not needed to install or use evo-dev.

This is a small personal configuration package. It does not enforce rules as an analyzer would, install Codex, configure models/MCP/plugins, or publish itself. Plugin packaging can wait until distribution warrants it.
