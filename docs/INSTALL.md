# Installation

Use the latest GitHub Release unless you are testing an unreleased change.

## Claude

1. Download the latest `i-have-adhd-and-47-tabs.zip` release asset.
2. Enable **Code execution and file creation** in **Settings → Capabilities**.
3. Open **Customize → Skills**.
4. Select **+ → Create skill → Upload a skill**.
5. Upload the ZIP and enable the skill.

Claude requires a ZIP containing one top-level folder whose name matches the skill name. That folder must contain `SKILL.md`.

Official documentation: https://support.claude.com/en/articles/12512180-use-skills-in-claude

## ChatGPT Skills

1. Download the latest `i-have-adhd-and-47-tabs.zip` release asset.
2. Open **Plugins** in the ChatGPT sidebar.
3. Select **Skills → Create → Upload from your computer**.
4. Upload the ZIP.

Personal Skills availability and workspace permissions can vary.

Official documentation: https://help.openai.com/en/articles/20001066

## Codex

Ask Codex's built-in skill installer to install the skill folder from this repository:

```text
$skill-installer install https://github.com/zgbrenner/i-have-adhd-and-47-tabs/tree/main/i-have-adhd-and-47-tabs
```

Restart Codex after installation so it discovers the new skill.

## GitHub Copilot

With GitHub CLI 2.90.0 or later:

```bash
gh skill preview zgbrenner/i-have-adhd-and-47-tabs i-have-adhd-and-47-tabs
gh skill install zgbrenner/i-have-adhd-and-47-tabs i-have-adhd-and-47-tabs --scope user
```

Omit `--scope user` to install it only for the current project.

Official documentation: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

## Universal Skills CLI

```bash
npx skills add zgbrenner/i-have-adhd-and-47-tabs
```

## Custom GPT fallback

1. Open **Explore GPTs → Create → Configure**.
2. Copy `chatgpt-custom-gpt/INSTRUCTIONS.md` into **Instructions**.
3. Add the included conversation starters.
4. Test in Preview and save.

Official documentation: https://help.openai.com/en/articles/8554397-use-advanced-data-analysis-in-chatgpt
