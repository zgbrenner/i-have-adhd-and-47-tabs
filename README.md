<p align="center">
  <strong style="font-size: 2rem;">I Have ADHD and 47 Tabs</strong>
</p>

<p align="center">
  <strong>Action-first AI for work, research, life, and every tab you forgot was open.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-2ea44f.svg"></a>
  <a href="dist/i-have-adhd-and-47-tabs.zip"><img alt="Download Skill" src="https://img.shields.io/badge/download-skill.zip-6f42c1.svg"></a>
  <img alt="Claude compatible" src="https://img.shields.io/badge/Claude-custom%20skill-D97757.svg">
  <img alt="ChatGPT compatible" src="https://img.shields.io/badge/ChatGPT-skill%20%2B%20GPT-10A37F.svg">
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-blue.svg">
</p>

<p align="center">
  <em>Your brain has enough tabs open. Your AI does not need to add twelve more.</em>
</p>

---

## The two-minute version

Most AI answers are technically correct and operationally useless. They begin with a preamble, hide the actual answer in paragraph four, hand you eleven equally weighted options, and end with “hope this helps.”

**I Have ADHD and 47 Tabs** changes the shape of the answer:

1. The answer or next action comes first.
2. Multi-step work becomes small numbered actions.
3. Long lists are capped, grouped, and ranked.
4. Context is restated when a project spans multiple turns.
5. The response ends when the useful part ends.

It works for **research, studying, writing, planning, email, administrative work, life logistics, and technical tasks**. It is a response-formatting skill, not a medical tool, and no diagnosis is required.

## Before and after

<table>
<tr>
<td width="50%" valign="top">

### Before

> Great question! There are several ways to approach planning your week. You may want to think about your priorities, deadlines, energy levels, meetings, errands, and personal obligations. One strategy is time blocking, while another is using a prioritized task list. You could also consider reviewing your calendar first...

</td>
<td width="50%" valign="top">

### After

> **Open your calendar and block the three deadlines first.**
>
> 1. Add anything due this week.
> 2. Reserve one work block for each deadline.
> 3. Put errands into one shared block.
> 4. Leave one unscheduled recovery block.
>
> Next: open your calendar and add the nearest deadline.

</td>
</tr>
</table>

## Download

**[Download the ready-to-upload ZIP](dist/i-have-adhd-and-47-tabs.zip)**

The ZIP contains exactly one top-level folder named `i-have-adhd-and-47-tabs`, with the required `SKILL.md` and supporting files inside it.

## Install in Claude

Claude custom skills are available on Free, Pro, Max, Team, and Enterprise plans when code execution is enabled.

1. Download [`dist/i-have-adhd-and-47-tabs.zip`](dist/i-have-adhd-and-47-tabs.zip).
2. In Claude, enable **Code execution and file creation** under **Settings → Capabilities**.
3. Open **Customize → Skills**.
4. Select **+ → Create skill → Upload a skill**.
5. Upload the ZIP and enable **I Have ADHD and 47 Tabs**.

Official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Install in ChatGPT Skills

Personal Skills are generally available for ChatGPT Business, Enterprise, Healthcare, and Edu. Availability and workspace permissions can vary.

1. Download [`dist/i-have-adhd-and-47-tabs.zip`](dist/i-have-adhd-and-47-tabs.zip).
2. Open **Plugins** in the ChatGPT sidebar.
3. Select **Skills → Create → Upload from your computer**.
4. Upload the ZIP.

OpenAI Skills follow the Agent Skills open standard, so the same package can be used across supported products.

Official guide: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

## ChatGPT Plus / Custom GPT fallback

When native Personal Skills are not available on your plan, create a Custom GPT:

1. Open **Explore GPTs → Create → Configure**.
2. Name it **I Have ADHD and 47 Tabs**.
3. Copy [`chatgpt-custom-gpt/INSTRUCTIONS.md`](chatgpt-custom-gpt/INSTRUCTIONS.md) into the GPT’s **Instructions** field.
4. Add the suggested conversation starters from that file.
5. Test it in Preview, then save or publish it.

Behavior belongs in the GPT’s Instructions field—not in Knowledge files. Official guide: [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-use-advanced-data-analysis-in-chatgpt).

## What is different from the original?

This project is a browser-first, general-purpose adaptation of **[Ayoub Ghriss’s original `i-have-adhd`](https://github.com/ayghri/i-have-adhd)** skill.

The original is optimized for coding agents. This adaptation keeps the core idea and ten-rule structure, then broadens the examples and behavior for:

- everyday questions and decisions;
- research and knowledge work;
- school and studying;
- writing, email, and administrative work;
- planning, errands, and personal logistics;
- technical work when needed.

The most important adaptation is subtle: factual questions lead with the **answer**, while tasks lead with the **next action**.

## The rules

1. Lead with the answer or next action.
2. Number multi-step tasks.
3. End with one concrete next step when work remains.
4. Suppress tangents.
5. Restate workflow state across turns.
6. Use concrete time estimates when useful.
7. Make progress and wins visible.
8. Describe errors matter-of-factly.
9. Keep lists short, grouped, and ranked.
10. Remove preambles, recaps, and empty closers.

The full instructions live in [`i-have-adhd-and-47-tabs/SKILL.md`](i-have-adhd-and-47-tabs/SKILL.md).

## Repository map

```text
i-have-adhd-and-47-tabs/
├── i-have-adhd-and-47-tabs/      # Uploadable skill source
│   ├── SKILL.md
│   ├── README.md
│   ├── LICENSE
│   ├── NOTICE.md
│   └── references/examples.md
├── chatgpt-custom-gpt/           # Fallback for Custom GPT users
├── dist/                         # Ready-to-upload ZIP
├── docs/                         # Installation and design notes
├── scripts/                      # Validation and reproducible packaging
├── tests/                        # Package contract tests
└── .github/                      # CI and contribution templates
```

## Build and validate

No third-party packages are required.

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
```

Or use:

```bash
make check
```

## Contributing

Small, concrete improvements are welcome—especially better examples, clearer trigger wording, and verified installation notes. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

## Attribution

**Original concept and skill:** [Ayoub Ghriss — `ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd)

**Browser/general-purpose adaptation:** [Zachary Brenner](https://github.com/zgbrenner)

The original copyright notice is preserved in [`LICENSE`](LICENSE) and the adaptation history is documented in [`NOTICE.md`](NOTICE.md).

## License

MIT. Use it, fork it, remix it, and close at least one tab.
