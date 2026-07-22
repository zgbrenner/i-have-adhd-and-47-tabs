# Contributing

Contributions should make the skill easier to trigger, easier to follow, safer to share, or easier to install.

You do not need to be a developer to contribute. Clear examples, installation testing, accessibility feedback, translations, and reports of confusing behavior are all valuable.

## Ways to contribute

- Add a realistic before-and-after example.
- Report an installation change in Claude, ChatGPT, Codex, or GitHub Copilot.
- Describe a case where the skill triggered too often or failed to trigger.
- Improve accessibility, clarity, or support for different attention styles.
- Translate the skill and user documentation.
- Improve validation, packaging, release automation, or security documentation.

Questions and early ideas belong in [GitHub Discussions](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/discussions). Reproducible bugs and scoped changes belong in [Issues](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/issues).

## Make a no-code contribution

1. Open the Markdown file you want to improve.
2. Select the pencil icon in the upper-right corner.
3. Make one focused change.
4. Select **Propose changes**.
5. Open the pull request and explain what becomes clearer or easier.

A maintainer can run packaging and validation for documentation-only contributions when needed.

## Source of truth

Edit the source files inside `i-have-adhd-and-47-tabs/`.

Do not manually edit `dist/i-have-adhd-and-47-tabs.zip`. The ZIP is generated from the source package by `python3 scripts/build_zip.py`, and CI verifies that the committed ZIP matches the source byte-for-byte.

Repository-level installation, community, and release documentation lives at the repository root and in `docs/`.

## Content guardrails

Contributions must:

1. Preserve the upstream attribution to Ayoub Ghriss.
2. Keep the ten-rule behavioral structure recognizable.
3. Avoid medical, diagnostic, or treatment claims.
4. Avoid presenting one ADHD experience as universal.
5. Preserve accuracy, citations, safety information, and necessary nuance.
6. Avoid turning “ADHD-friendly” into “always extremely short.”
7. Use realistic general-purpose examples, not only coding examples.
8. Keep the stop phrases and Custom GPT instructions synchronized when behavior changes.

## Translation contributions

Place each translation in a language folder under `translations/`, using a BCP 47 language tag where practical:

```text
translations/es/
translations/fr/
translations/de/
translations/pt-BR/
```

A translation should include:

- a translated `SKILL.md`;
- a short translated README;
- a note identifying the source version;
- the original and adaptation attribution;
- a reviewer who is fluent in the target language, when available.

Preserve the behavioral meaning rather than translating every sentence literally.

## Before opening a pull request

1. Keep the change focused.
2. Add or update a test when changing package behavior.
3. Update documentation when an installation path changes.
4. Run `make check`.
5. Explain the user-visible effect in the pull request.
6. Confirm that no credentials, personal data, or generated cache files are included.

## Local checks

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
```

No third-party Python packages are required.

By contributing, you agree that your contribution will be licensed under the repository's MIT License.
