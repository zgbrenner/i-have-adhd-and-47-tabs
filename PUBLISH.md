# Publishing

## Publish repository changes

Install and authenticate GitHub CLI, then run:

```bash
./scripts/publish_to_github.sh
```

The script validates the skill, rebuilds the distributable ZIP, runs tests, commits resulting changes, verifies the `origin` repository, and pushes the current branch.

## Publish a release

Releases are automated from the `VERSION` file.

1. Update `VERSION`, `i-have-adhd-and-47-tabs/SKILL.md`, `CITATION.cff`, `CHANGELOG.md`, and `docs/releases/<version>.md`.
2. Run `make check`.
3. Merge the change to `main`.

A GitHub Actions workflow tags the merge commit, rebuilds the ZIP, generates `SHA256SUMS`, and publishes both as GitHub Release assets. It exits without changing anything when the release already exists.

## Manual validation

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
git diff --exit-code -- dist/i-have-adhd-and-47-tabs.zip
```
