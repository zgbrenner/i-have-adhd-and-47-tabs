#!/usr/bin/env bash
set -euo pipefail

REPO="zgbrenner/i-have-adhd-and-47-tabs"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

for command in git gh python3; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command" >&2
    exit 1
  fi
done

if ! gh auth status >/dev/null 2>&1; then
  echo "Authenticate first with: gh auth login" >&2
  exit 1
fi

VERSION="$(tr -d '[:space:]' < VERSION)"
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "VERSION must contain a semantic version such as 1.1.0" >&2
  exit 1
fi

TAG="v$VERSION"
NOTES="docs/releases/$VERSION.md"
ZIP="dist/i-have-adhd-and-47-tabs.zip"
CHECKSUMS="dist/SHA256SUMS"

test -f "$NOTES" || { echo "Missing release notes: $NOTES" >&2; exit 1; }

make check

git diff --exit-code -- "$ZIP"

python3 - "$ZIP" "$CHECKSUMS" <<'PY'
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
digest = hashlib.sha256(source.read_bytes()).hexdigest()
target.write_text(f"{digest}  {source.name}\n", encoding="utf-8")
PY

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "The working tree has uncommitted changes. Commit and push them before releasing." >&2
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "Releases must be created from main; current branch is '$CURRENT_BRANCH'." >&2
  exit 1
fi

git fetch origin main --tags
if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
  echo "Local main is not identical to origin/main. Pull or push before releasing." >&2
  exit 1
fi

if ! git rev-parse "$TAG" >/dev/null 2>&1; then
  git tag -a "$TAG" -m "I Have ADHD and 47 Tabs $VERSION"
  git push origin "$TAG"
fi

if gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
  gh release upload "$TAG" "$ZIP" "$CHECKSUMS" --clobber --repo "$REPO"
  gh release edit "$TAG" \
    --title "I Have ADHD and 47 Tabs $TAG" \
    --notes-file "$NOTES" \
    --latest \
    --repo "$REPO"
else
  gh release create "$TAG" \
    "$ZIP" \
    "$CHECKSUMS" \
    --verify-tag \
    --title "I Have ADHD and 47 Tabs $TAG" \
    --notes-file "$NOTES" \
    --latest \
    --repo "$REPO"
fi

printf 'Published %s: https://github.com/%s/releases/tag/%s\n' "$TAG" "$REPO" "$TAG"
