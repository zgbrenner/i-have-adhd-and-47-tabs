# Publish to GitHub

The repository is already initialized locally on `main` with a clean commit.

## One-command publish

Install and authenticate the GitHub CLI, then run:

```bash
./scripts/publish_to_github.sh
```

The script creates `zgbrenner/i-have-adhd-and-47-tabs` as a **public** repository, adds it as `origin`, and pushes `main`.

## Manual equivalent

```bash
gh auth login
gh repo create zgbrenner/i-have-adhd-and-47-tabs \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Action-first AI for work, research, life, and every tab you forgot was open."
```

After publishing, confirm that the repository is public and that `dist/i-have-adhd-and-47-tabs.zip` is visible for direct download.
