# Publish to GitHub

## One-command publish

Install and authenticate the GitHub CLI, then run:

```bash
./scripts/publish_to_github.sh
```

The script validates the skill, rebuilds the distributable ZIP, runs the tests, commits any resulting changes, verifies that `origin` targets the expected repository, and pushes the current branch. If the repository does not exist yet, it creates it as a public repository first.

## Manual equivalent

```bash
gh auth login
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
git add --all
git commit -m "Refresh validated skill package"
BRANCH="$(git branch --show-current)"
git push -u origin "$BRANCH"
```

For a first-time publication, create the repository with:

```bash
gh repo create zgbrenner/i-have-adhd-and-47-tabs \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Action-first AI for work, research, life, and every tab you forgot was open."
```

After publishing, confirm that the repository is public and that `dist/i-have-adhd-and-47-tabs.zip` is visible for direct download.
