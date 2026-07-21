# Design notes

## Goal

Make the original action-first ADHD response style useful outside coding agents, especially in browser-based Claude and ChatGPT conversations.

## Design choices

### Answer or action first

The upstream skill leads with the next action. That is ideal for tasks but can distort factual questions. This adaptation leads with the **answer** for knowledge questions and the **next action** for tasks.

### General-purpose examples

Examples cover everyday information, research, studying, writing, planning, and errors. Technical behavior remains supported but is no longer the assumed context.

### Same package, honest platform differences

The ZIP follows the shared Agent Skills structure for Claude and supported ChatGPT Skills. A separate instruction file is provided for Custom GPTs because a Custom GPT is not the same product surface as a native Skill.

### Minimal dependencies

The skill itself contains no executable code and requires no external package. Repository scripts use only the Python standard library.
