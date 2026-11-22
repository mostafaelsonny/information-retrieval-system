# ==============================================================================
# setup_github.ps1 — Automated GitHub Repository Setup for PowerShell (Windows)
# ==============================================================================
param (
    [string]$RepoName = "information-retrieval-system",
    [string]$Visibility = "public"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Checking Git and GitHub CLI..." -ForegroundColor Cyan
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is not installed or not in PATH"
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed. Download from https://cli.github.com"
}

Set-Location "$PSScriptRoot\.."

Write-Host "📦 Initializing local Git repository..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    git init -b main
}

git add -A
git commit -m "chore: initial project scaffold and governance foundation" -ErrorAction SilentlyContinue

Write-Host "🌐 Creating GitHub repository '$RepoName' ($Visibility)..." -ForegroundColor Cyan
gh repo create "$RepoName" "--$Visibility" --source=. --remote=origin --push

Write-Host "🌿 Setting up 'develop' integration branch..." -ForegroundColor Cyan
git checkout -B develop
git push -u origin develop
gh repo edit --default-branch develop

Write-Host "🏷️ Creating Trello-aligned labels..." -ForegroundColor Cyan
function Add-Label($name, $color, $desc) {
    gh label create "$name" --color "$color" --description "$desc" --force | Out-Null
}

Add-Label "leader"        "10b981" "Leader & Integration tasks (Mostafa)"
Add-Label "preprocessing" "f97316" "Data loading & PySpark positional index (Monzer)"
Add-Label "statistics"    "eab308" "TF, WTF, DF, IDF statistics (Ebrahim)"
Add-Label "vectorization" "3b82f6" "TF-IDF matrix & L2 normalization (Rovan)"
Add-Label "retrieval"     "a855f7" "Phrase, Boolean queries & ranking (Febronia)"
Add-Label "milestone"     "ef4444" "Critical project milestones"
Add-Label "bug"           "d73a4a" "Something is not working or math error"
Add-Label "task"          "ededed" "Sprint card task"

Write-Host "🎯 Creating Sprint Hourly Milestones..." -ForegroundColor Cyan
$milestones = @(
    "Hour 0-1: Foundation & Contracts",
    "Hour 1-2: Core Stubs & Parallel Dev",
    "Hour 2-3: Module Implementation",
    "Hour 3-4: Main Pipeline Integration",
    "Hour 4-5: Ground Truth Testing",
    "Hour 5-6: Documentation & Submission"
)
foreach ($m in $milestones) {
    gh api "repos/{owner}/{repo}/milestones" -f title="$m" 2>$null | Out-Null
}

Write-Host "🛡️ Applying branch protection rulesets..." -ForegroundColor Cyan
foreach ($b in @("main", "develop")) {
    try {
        gh api -X POST "repos/{owner}/{repo}/rulesets" --input ".github/rulesets/protect-$b.json" | Out-Null
        Write-Host "  ✅ Ruleset applied for $b" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️ Could not apply ruleset for $b automatically. Please import .github/rulesets/protect-$b.json manually." -ForegroundColor Yellow
    }
}

$repoUrl = gh repo view --json url -q .url
Write-Host "`n🎉 All Done! Repository is live at: $repoUrl" -ForegroundColor Green
