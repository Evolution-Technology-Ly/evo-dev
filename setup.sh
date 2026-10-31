#!/bin/sh
# Install missing files only. Existing differing files require manual review.
set -eu

evo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
evo_user_directory=${HOME:?HOME must identify your user directory}
evo_profile_only=false
while [ "$#" -gt 0 ]; do
    case "$1" in
        --profile-only) evo_profile_only=true; shift ;;
        --user-directory)
            if [ "$#" -lt 2 ] || [ -z "$2" ]; then
                printf '%s\n' '--user-directory requires a path' >&2
                exit 1
            fi
            evo_user_directory=$2; shift 2 ;;
        *)
            printf '%s\n' 'Usage: sh setup.sh [--profile-only] [--user-directory PATH]' >&2
            exit 1 ;;
    esac
done
evo_codex_directory=${CODEX_HOME:-"$evo_user_directory/.codex"}
evo_skill_directory="$evo_user_directory/.agents/skills/project-setup"
evo_status=0

conflict() {
    printf 'REVIEW: %s (preserved)\n' "$1"
    evo_status=1
}

install_missing() {
    evo_source=$1
    evo_target=$2
    if [ -e "$evo_target" ] || [ -L "$evo_target" ]; then
        evo_same_kind=false
        if [ -d "$evo_source" ] && [ -d "$evo_target" ]; then evo_same_kind=true; fi
        if [ -f "$evo_source" ] && [ -f "$evo_target" ]; then evo_same_kind=true; fi
        if [ "$evo_same_kind" = true ] && diff -r "$evo_source" "$evo_target" >/dev/null 2>&1; then
            printf 'UNCHANGED: %s\n' "$evo_target"
        else
            conflict "$evo_target differs from $evo_source"
        fi
        return
    fi
    mkdir -p "$(dirname -- "$evo_target")"
    if [ -d "$evo_source" ]; then
        mkdir "$evo_target"
        cp -R "$evo_source/." "$evo_target/"
    else
        # Noclobber also protects a file created between inspection and writing.
        (set -C; cat "$evo_source" > "$evo_target")
    fi
    printf 'INSTALLED: %s\n' "$evo_target"
}

# Check the package before making any installation changes.
test -f "$evo_root/profile/AGENTS.md"
if [ "$evo_profile_only" = false ]; then
    test -f "$evo_root/skills/project-setup/SKILL.md"
    test -f "$evo_root/skills/project-setup/agents/openai.yaml"
fi

install_missing "$evo_root/profile/AGENTS.md" "$evo_codex_directory/AGENTS.md"
if [ "$evo_profile_only" = false ]; then
    if [ -e "$evo_codex_directory/skills/project-setup" ] || [ -L "$evo_codex_directory/skills/project-setup" ]; then
        conflict "$evo_codex_directory/skills/project-setup already exists; review this alternate installation before adding another"
    else
        install_missing "$evo_root/skills/project-setup" "$evo_skill_directory"
    fi
fi
if [ -e "$evo_codex_directory/AGENTS.override.md" ] || [ -L "$evo_codex_directory/AGENTS.override.md" ]; then
    conflict "$evo_codex_directory/AGENTS.override.md exists; review whether it overrides the installed preferences"
fi

if [ "$evo_status" -eq 0 ]; then
    printf '%s\n' 'evo-dev is ready. Open a new Codex chat and invoke $project-setup.'
else
    printf '%s\n' 'Resolve REVIEW items manually and rerun setup. Missing items may have been installed; no existing files were replaced.'
fi
exit "$evo_status"
