# Wrapper for nuitka-release.sh using Git Bash (MINGW), not WSL.
# Run as:  ./nuitka-release.ps1 [args...]
[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments)] $Args)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$gitBash = (Get-Command bash -ErrorAction SilentlyContinue | Where-Object { $_.Source -match "Git" } | Select-Object -First 1).Source
if (-not $gitBash -and (Test-Path "$env:ProgramFiles\Git\bin\bash.exe")) { $gitBash = "$env:ProgramFiles\Git\bin\bash.exe" }
if (-not $gitBash -and (Test-Path "${env:ProgramFiles(x86)}\Git\bin\bash.exe")) { $gitBash = "${env:ProgramFiles(x86)}\Git\bin\bash.exe" }
if (-not $gitBash) { throw "Git Bash not found. Install Git for Windows or run nuitka-release.sh from a Git Bash shell." }

& $gitBash nuitka-release.sh @Args
