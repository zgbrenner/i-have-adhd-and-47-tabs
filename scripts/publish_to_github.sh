#!/usr/bin/env bash
set -euo pipefail

REPO="zgbrenner/i-have-adhd-and-47-tabs"
DESCRIPTION="Action-first AI for work, research, life, and every tab you forgot was open."
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI is required: https://cli.github.com/" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Authenticate first with: gh auth login" >&2
  exit 1
fi

python scripts/validate_skill.py
python scripts/build_zip.py
python -m unittest discover -s tests -v

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  git init -b main
  git config user.name "$(gh api user --jq '.name // .login')"
  git config user.email "$(gh api user --jq '.login')@users.noreply.github.com"
  git add .
  git commit -m "Initial release of I Have ADHD and 47 Tabs"
fi

if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "Repository already exists: https://github.com/$REPO"
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "https://github.com/$REPO.git"
  fi
  git push -u origin main
else
  gh repo create "$REPO" \
    --public \
    --source=. \
    --remote=origin \
    --push \
    --description "$DESCRIPTION"
fi

printf '\nPublished: https://github.com/%s\n' "$REPO"
