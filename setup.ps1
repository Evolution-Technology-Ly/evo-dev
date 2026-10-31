# Compatible with Windows PowerShell 5.1 and PowerShell 7.
param([string]$UserDirectory = $HOME, [switch]$ProfileOnly)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($UserDirectory)) { throw 'A user directory is required.' }
$evoRoot = $PSScriptRoot
$evoCodexDirectory = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $UserDirectory '.codex' }
$evoSkillDirectory = Join-Path $UserDirectory '.agents/skills/project-setup'
$script:evoStatus = 0

function Report-Conflict([string]$Message) {
    Write-Output "REVIEW: $Message (preserved)"
    $script:evoStatus = 1
}

function Get-DirectorySignature([string]$Directory) {
    $evoBase = (Get-Item -LiteralPath $Directory -Force).FullName.TrimEnd([IO.Path]::DirectorySeparatorChar)
    Get-ChildItem -LiteralPath $Directory -Recurse -File -Force | ForEach-Object {
        $evoRelative = $_.FullName.Substring($evoBase.Length + 1).Replace('\', '/')
        '{0} {1}' -f $evoRelative, (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    } | Sort-Object
}

function Install-Missing([string]$Source, [string]$Target) {
    $evoSourceIsDirectory = Test-Path -LiteralPath $Source -PathType Container
    # Get-Item also detects a dangling link, which must not be replaced.
    $evoExisting = Get-Item -LiteralPath $Target -Force -ErrorAction SilentlyContinue
    if ($null -ne $evoExisting) {
        $evoIdentical = $false
        if ($evoSourceIsDirectory -and (Test-Path -LiteralPath $Target -PathType Container)) {
            $evoSourceSignature = @(Get-DirectorySignature $Source)
            $evoTargetSignature = @(Get-DirectorySignature $Target)
            $evoIdentical = ($evoSourceSignature.Count -eq $evoTargetSignature.Count -and
                (@(Compare-Object $evoSourceSignature $evoTargetSignature -CaseSensitive)).Count -eq 0)
        } elseif (-not $evoSourceIsDirectory -and (Test-Path -LiteralPath $Target -PathType Leaf)) {
            $evoIdentical = ((Get-FileHash -LiteralPath $Source).Hash -eq (Get-FileHash -LiteralPath $Target).Hash)
        }
        if ($evoIdentical) { Write-Output "UNCHANGED: $Target" }
        else { Report-Conflict "$Target differs from $Source" }
        return
    }
    [IO.Directory]::CreateDirectory((Split-Path -Parent $Target)) | Out-Null
    if ($evoSourceIsDirectory) {
        [IO.Directory]::CreateDirectory($Target) | Out-Null
        $evoBase = (Get-Item -LiteralPath $Source).FullName
        Get-ChildItem -LiteralPath $Source -Recurse -File -Force | ForEach-Object {
            $evoDestination = Join-Path $Target $_.FullName.Substring($evoBase.Length + 1)
            [IO.Directory]::CreateDirectory((Split-Path -Parent $evoDestination)) | Out-Null
            [IO.File]::Copy($_.FullName, $evoDestination, $false)
        }
    } else {
        [IO.File]::Copy($Source, $Target, $false)
    }
    Write-Output "INSTALLED: $Target"
}

$evoRequiredFiles = @('profile/AGENTS.md')
if (-not $ProfileOnly) { $evoRequiredFiles += @('skills/project-setup/SKILL.md', 'skills/project-setup/agents/openai.yaml') }
foreach ($evoRequired in $evoRequiredFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $evoRoot $evoRequired) -PathType Leaf)) {
        throw "Missing package file: $evoRequired"
    }
}
Install-Missing (Join-Path $evoRoot 'profile/AGENTS.md') (Join-Path $evoCodexDirectory 'AGENTS.md')
if (-not $ProfileOnly) {
    $evoAlternate = Join-Path $evoCodexDirectory 'skills/project-setup'
    if ($null -ne (Get-Item -LiteralPath $evoAlternate -Force -ErrorAction SilentlyContinue)) {
        Report-Conflict "$evoAlternate already exists; review this alternate installation before adding another"
    } else {
        Install-Missing (Join-Path $evoRoot 'skills/project-setup') $evoSkillDirectory
    }
}
$evoOverride = Join-Path $evoCodexDirectory 'AGENTS.override.md'
if ($null -ne (Get-Item -LiteralPath $evoOverride -Force -ErrorAction SilentlyContinue)) {
    Report-Conflict "$evoOverride exists; review whether it overrides the installed preferences"
}
if ($script:evoStatus -eq 0) {
    Write-Output 'evo-dev is ready. Open a new Codex chat and invoke $project-setup.'
} else {
    Write-Output 'Resolve REVIEW items manually and rerun setup. Missing items may have been installed; no existing files were replaced.'
}
exit $script:evoStatus
