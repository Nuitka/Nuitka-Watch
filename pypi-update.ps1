# Wrapper for pypi-update.sh using Git Bash (MINGW), not WSL.
# Run as:  ./pypi-update.ps1 [args...]
[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments)] $Args)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$gitBash = (Get-Command bash -ErrorAction SilentlyContinue | Where-Object { $_.Source -match "Git" } | Select-Object -First 1).Source
if (-not $gitBash -and (Test-Path "$env:ProgramFiles\Git\bin\bash.exe")) { $gitBash = "$env:ProgramFiles\Git\bin\bash.exe" }
if (-not $gitBash -and (Test-Path "${env:ProgramFiles(x86)}\Git\bin\bash.exe")) { $gitBash = "${env:ProgramFiles(x86)}\Git\bin\bash.exe" }
if (-not $gitBash) { throw "Git Bash not found. Install Git for Windows or run pypi-update.sh from a Git Bash shell." }

& $gitBash pypi-update.sh @Args
