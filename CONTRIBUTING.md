# Contributing

Contributions should make the skill easier to trigger, easier to follow, or easier to install.

## Good contributions

- clearer examples for research, school, writing, planning, or everyday work;
- fixes for verified Claude or ChatGPT installation changes;
- tighter wording that preserves accuracy and accessibility;
- validation improvements that catch broken packages;
- translations that preserve the behavioral intent.

## Before opening a pull request

1. Keep the core ten-rule structure recognizable.
2. Preserve the upstream attribution to Ayoub Ghriss.
3. Add or update a test when changing package behavior.
4. Run `make check`.
5. Explain the user-visible effect in the pull request.

## Local checks

```bash
python scripts/validate_skill.py
python scripts/build_zip.py
python -m unittest discover -s tests -v
```

No third-party dependencies are required.
