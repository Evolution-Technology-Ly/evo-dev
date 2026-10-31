# evo-dev

Minimal Codex development configuration for **Evolution Technology**: personal preferences and explicit repository onboarding, based on the EvoCommerce pilot.

## Install through a Git-backed marketplace

No manual clone is needed. With Git and the Codex CLI available, run these commands once on macOS, Windows PowerShell, or Linux:

```text
codex plugin marketplace add Evolution-Technology-Ly/evo-dev
codex plugin add evo-dev@evo-dev
```

Codex downloads and caches the package. Open a new Codex desktop or CLI chat and explicitly select **Evo Dev Setup**, or invoke its skill:

```text
$evo-dev:evo-setup
```

The plugin declares this as its onboarding skill, so supported desktop versions can also expose it through the plugin's setup action. Codex namespaces the bundled skills with `evo-dev:`; you can also select their display names in the skill picker.

If `codex` is not on your terminal PATH, you can ask Codex in the desktop app:

> Register https://github.com/Evolution-Technology-Ly/evo-dev as a Git-backed plugin marketplace using the bundled Codex CLI, then install evo-dev from that marketplace. Preserve other configuration.

Then start a new chat and select Evo Dev Setup. This uses Codex's own package download, rather than asking you to maintain a checkout. A desktop client without access to the bundled CLI can use a separately installed Codex CLI for registration.

The source is public; fetching it requires no GitHub organization membership. This is a custom Git-backed marketplace, not a listing in OpenAI's public plugin directory. Desktop/CLI plugin support and installation commands follow the [official plugin guide](https://developers.openai.com/plugins/build/plugins) and [command reference](https://learn.chatgpt.com/docs/developer-commands). The IDE extension currently does not support plugins; use the standalone fallback below for that client.

## What setup changes

Installing the plugin makes its two skills available. It does not automatically write your personal profile. Running Evo Dev Setup invokes the packaged installer in **profile-only mode**:

| Item | Location |
| --- | --- |
| [Personal preferences](profile/AGENTS.md) | `~/.codex/AGENTS.md`, or `CODEX_HOME/AGENTS.md` when configured |
| [Evo Dev Setup](skills/evo-setup/SKILL.md) and [Project Setup](skills/project-setup/SKILL.md) | Managed by Codex in the installed plugin cache |

The installer copies only a missing profile, skips identical content, and **preserves differing files and links**. It leaves `config.toml`, credentials, other plugins/skills, project code, and checkpoints alone. `REVIEW` output means manual reconciliation is needed; setup exits nonzero and does not overwrite the existing item. Existing `AGENTS.override.md` is reported because it can take precedence over the profile.

Both skills are explicit-only (`allow_implicit_invocation: false`). No hooks, MCP servers, background services, or additional runtimes are required. Profile setup uses the system shell on macOS/Linux and PowerShell on Windows. The Windows installer uses a process-scoped execution-policy argument, not a permanent policy change.

If you previously installed standalone project-setup, review local customizations and choose one installation method before using the plugin. Evo Dev Setup reports possible duplicates and preserves them; it never deletes an existing skill or link automatically. The original Mac pilot remains a standalone installation until deliberately migrated.

## Work in an existing project

After profile setup, start a new chat in the project's actual Git root (for example the backend repository, rather than its parent directory). Invoke or select:

```text
$evo-dev:project-setup
```

You may add a scope: `$evo-dev:project-setup Focus on the backend.` It inspects current implementation, representative tests, existing instructions, and Git before creating or improving concise AGENTS.md guidance. It preserves useful rules and existing work; a checkpoint is created only for a real task continuity need. It carries no EvoCommerce-specific architecture or business rules.

Review the documentation diff, then describe normal development tasks. Rerun Project Setup only to onboard another repository or deliberately refresh its guidance. Repository instructions and task checkpoints stay with their projects; evo-dev does not synchronize uncommitted code or conversations. Scoped project instructions take precedence over personal defaults as described in the [official instruction guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Update

For maintainers: bump the version in `plugin.json` when publishing changes to bundled skills or setup behavior.

Refresh the Git-backed marketplace:

```text
codex plugin marketplace upgrade evo-dev
```

Then reinstall/update Evo Dev from that source using the plugin browser or `codex plugin add evo-dev@evo-dev`, and open a new chat. Rerun Evo Dev Setup if you want to reconcile updated preferences. An installed global profile is a copy: differences require a deliberate merge and are never silently replaced. Edit reusable preferences in `profile/AGENTS.md`; changes made directly to a machine's global profile must be reconciled back into this repository deliberately.

## Standalone fallback

For the IDE extension or users who prefer a checkout, clone the repository and run from its root:

```sh
# macOS/Linux
sh ./setup.sh
```

```powershell
# Windows
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

This installs the profile and standalone project-setup under `~/.agents/skills/project-setup/`. It does not install the plugin or Evo Dev Setup. Existing differing files are preserved and reported; identical content is skipped. Existing matching links from the Mac pilot remain intact. To install only the profile from a checkout, use `--profile-only` or `-ProfileOnly` respectively. Do not run full standalone setup alongside the plugin, since that creates another copy of Project Setup.

For isolated checks, `--user-directory PATH` / `-UserDirectory PATH` redirects the target user directory. `CODEX_HOME`, when set, still takes precedence for the profile. The installer does not install Codex, configure models, or download dependencies.

## Validate

With Python 3 available for development checks:

```sh
python3 -m unittest discover -s tests -v
```

On Windows use `py -3` instead of `python3`. The tests use temporary user directories, exercise available shells, and explicitly skip unavailable shells. Set `EVO_CODEX_BINARY` to a Codex executable to include the native marketplace/package installation check. Python is not required to install or use evo-dev. Passing on one OS does not prove native behavior on other operating systems.
