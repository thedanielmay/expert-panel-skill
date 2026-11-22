# Fact pass for skill review

You measure and report. You judge nothing. Change no file in the repo. Write only `{OUT}`.

- Repo: {REPO}
- SKILL.md: {SKILLMD}

Report these, each figure with the command that produced it:

1. Inventory: tracked files (`git ls-files`) with line counts, and which files `SKILL.md` points to.
2. Frontmatter: name, description length in characters, trigger phrases, version, whether a personal mark is set (`metadata.personal`).
3. Cost: bytes and an estimate of tokens (characters divided by 4) for `SKILL.md` and each file it points to.
4. Broken references: every file path, command and flag in the text, checked with `test -e`, `command -v` or the command's `--help`. List what exists and what does not. Never run a command that changes anything.
5. Owner-specific text: matches for home-directory paths (the system users folder, `~/`), email addresses, and named people or organisations. List them. Do not judge them.
6. Repetition and contradictions: quote both lines with `file:line`.
7. Heading map: each heading with its start line and the number of lines to the next heading.
8. The repo's own checker, if one exists (a script named like `check`, `validate` or `lint`): run it read only and quote its last lines.

Write plain facts in bullets. No opinions, no advice.
