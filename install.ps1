# Install Cursor skills from this repo into %USERPROFILE%\.cursor\skills (or a custom dest).
# Default: directory junction/symlink when possible; use -Copy for a snapshot.
[CmdletBinding()]
param(
    [ValidateSet("symlink", "copy")]
    [string]$Mode = "symlink",

    [string]$Dest = $(if ($env:CURSOR_SKILLS_DIR) { $env:CURSOR_SKILLS_DIR } else { Join-Path $HOME ".cursor\skills" }),

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Skills,

    [switch]$List
)

$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot

$DefaultSkills = @(
    "golang-development",
    "golang-code-review",
    "context-discovery"
)

function Get-InstallableSkills {
    Get-ChildItem -Path $RepoRoot -Directory | Where-Object {
        Test-Path (Join-Path $_.FullName "SKILL.md")
    } | ForEach-Object { $_.Name }
}

if ($List) {
    Write-Host "Default skills:"
    $DefaultSkills | ForEach-Object { Write-Host "  - $_" }
    Write-Host ""
    Write-Host "Also in repo (pass by name to install):"
    Get-InstallableSkills | Where-Object { $_ -notin $DefaultSkills } | ForEach-Object {
        Write-Host "  - $_"
    }
    exit 0
}

if (-not $Skills -or $Skills.Count -eq 0) {
    $Skills = $DefaultSkills
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

Write-Host "Repo:  $RepoRoot"
Write-Host "Dest:  $Dest"
Write-Host "Mode:  $Mode"
Write-Host ""

foreach ($name in $Skills) {
    $src = Join-Path $RepoRoot $name
    $skillMd = Join-Path $src "SKILL.md"
    if (-not (Test-Path $skillMd)) {
        throw "Not a skill (missing SKILL.md): $name"
    }

    $target = Join-Path $Dest $name
    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
    }

    if ($Mode -eq "symlink") {
        try {
            New-Item -ItemType SymbolicLink -Path $target -Target $src | Out-Null
        } catch {
            # Fallback when symlink requires elevation: directory junction (same volume)
            New-Item -ItemType Junction -Path $target -Target $src | Out-Null
        }
        Write-Host "linked  $name -> $src"
    } else {
        Copy-Item -Recurse -Path $src -Destination $target
        Write-Host "copied  $name -> $target"
    }

    if (-not (Test-Path (Join-Path $target "SKILL.md"))) {
        throw "Install failed for $name (SKILL.md not reachable)"
    }
}

Write-Host ""
Write-Host "Done. Restart Cursor or open a new Agent chat."
Write-Host "Verify: Get-ChildItem `"$Dest`""
