#!/usr/bin/env bash
# ==============================================================================
# setup_github.sh — Automated GitHub Repository Setup & Governance Script
# ==============================================================================
# Usage:
#   ./scripts/setup_github.sh [repo-name] [public|private]
# Example:
#   ./scripts/setup_github.sh information-retrieval-system public
# ==============================================================================
set -euo pipefail

REPO_NAME="${1:-information-retrieval-system}"
VISIBILITY="${2:-public}"

command -v git >/dev/null || { echo "❌ git is not installed"; exit 1; }
command -v gh  >/dev/null || { echo "❌ Install GitHub CLI first: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || gh auth login

cd "$(dirname "$0")/.."

echo "🚀 Initializing Git repository..."
if [ ! -d .git ]; then
  git init -b main
fi

git add -A
git commit -m "chore: initial project scaffold and governance foundation" || echo "(nothing new to commit)"

echo "📦 Creating GitHub repository '$REPO_NAME' ($VISIBILITY)..."
gh repo create "$REPO_NAME" "--$VISIBILITY" --source=. --remote=origin --push

echo "🌿 Setting up 'develop' integration branch..."
git checkout -B develop
git push -u origin develop
gh repo edit --default-branch develop

echo "🏷️ Configuring Trello-aligned labels..."
mk_label() { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
mk_label "leader"        "10b981" "Leader & Integration tasks (Mostafa)"
mk_label "preprocessing" "f97316" "Data loading & PySpark positional index (Monzer)"
mk_label "statistics"    "eab308" "TF, WTF, DF, IDF statistics (Ebrahim)"
mk_label "vectorization" "3b82f6" "TF-IDF matrix & L2 normalization (Rovan)"
mk_label "retrieval"     "a855f7" "Phrase, Boolean queries & ranking (Febronia)"
mk_label "milestone"     "ef4444" "Critical project milestones"
mk_label "bug"           "d73a4a" "Something is not working or math error"
mk_label "task"          "ededed" "Sprint card task"

echo "🎯 Creating Hourly Sprint Milestones..."
for h in "Hour 0-1: Foundation & Contracts" \
         "Hour 1-2: Core Stubs & Parallel Dev" \
         "Hour 2-3: Module Implementation" \
         "Hour 3-4: Main Pipeline Integration" \
         "Hour 4-5: Ground Truth Testing" \
         "Hour 5-6: Documentation & Submission"; do
  gh api "repos/{owner}/{repo}/milestones" -f title="$h" >/dev/null || true
done

echo "🛡️ Applying branch protection rulesets (protect-main & protect-develop)..."
for b in main develop; do
  gh api -X POST "repos/{owner}/{repo}/rulesets" --input ".github/rulesets/protect-$b.json" >/dev/null \
    && echo "✅ Ruleset applied: protect-$b" \
    || echo "⚠️ WARN: Could not apply ruleset for '$b'. Please import .github/rulesets/protect-$b.json manually."
done

echo "🎉 Done! Repository URL: $(gh repo view --json url -q .url)"
