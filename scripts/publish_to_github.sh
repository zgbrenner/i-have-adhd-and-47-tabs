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

python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  git init -b main
  git config user.name "$(gh api user --jq '.name // .login')"
  git config user.email "$(gh api user --jq '.login')@users.noreply.github.com"
fi

if git remote get-url origin >/dev/null 2>&1; then
  ORIGIN_REPO="$(gh repo view "$(git remote get-url origin)" --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null || true)"
  if [[ "$ORIGIN_REPO" != "$REPO" ]]; then
    echo "Refusing to publish: origin points to '${ORIGIN_REPO:-an unrecognized repository}', expected '$REPO'." >&2
    exit 1
  fi
elif gh repo view "$REPO" >/dev/null 2>&1; then
  git remote add origin "https://github.com/$REPO.git"
fi

git add --all
if ! git diff --cached --quiet; then
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    git commit -m "Refresh validated skill package"
  else
    git commit -m "Initial release of I Have ADHD and 47 Tabs"
  fi
fi

BRANCH="$(git branch --show-current)"
if [[ -z "$BRANCH" ]]; then
  echo "Cannot publish from a detached HEAD. Check out a branch first." >&2
  exit 1
fi

if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "Repository already exists: https://github.com/$REPO"
  git push -u origin "$BRANCH"
else
  gh repo create "$REPO" \
    --public \
    --source=. \
    --remote=origin \
    --push \
    --description "$DESCRIPTION"
fi

printf '\nPublished: https://github.com/%s/tree/%s\n' "$REPO" "$BRANCH"
