# Publishing

This repository intentionally uses no GitHub Actions or hosted CI. Validation, packaging, pushes, and releases run from a maintainer's computer.

## One-time setup

Install Python 3, Git, and GitHub CLI, then authenticate:

```bash
gh auth login
make install-hooks
```

The optional Git hook runs `make check` before each push on that computer.

## Publish repository changes

```bash
./scripts/publish_to_github.sh
```

The script validates the skill, rebuilds the distributable ZIP, runs tests, commits resulting changes, verifies the `origin` repository, and pushes the current branch.

## Publish a release

1. Update `VERSION`, `i-have-adhd-and-47-tabs/SKILL.md`, `CITATION.cff`, `CHANGELOG.md`, and `docs/releases/<version>.md`.
2. Run `make check`.
3. Commit and push the changes to `main`.
4. Run:

```bash
make release
```

The local release script:

- validates the version and release notes;
- runs the complete repository test suite;
- confirms the committed ZIP is current;
- generates `dist/SHA256SUMS` locally;
- verifies local `main` matches `origin/main`;
- creates and pushes the annotated version tag when needed;
- creates or updates the GitHub Release and its two assets.

It uses the GitHub API through the authenticated `gh` command and does not start a GitHub Actions job.

## Manual validation

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
git diff --exit-code -- dist/i-have-adhd-and-47-tabs.zip
```
