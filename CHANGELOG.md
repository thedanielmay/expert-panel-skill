# Changelog

## 1.3.0 - 2026-11-26

- Split the skill into a router and a panel reference.
  - `SKILL.md` now holds the frontmatter, core principle, mode routing, severity rule and reference list.
  - A panel run reads `references/panel.md` in full before it starts.
  - A skill review run reads `references/skill-review.md`. It does not load the panel text.
- Moved the panel workflow to `references/panel.md` word for word.
  - Stages 1 and 2, both workflows, the claim check, the dossier inputs, the output format and the expert behaviour rules moved.
  - The four panel flags now sit in the routing section of `SKILL.md`.
- Updated `README.md` for the new file layout.

## 1.2.0 - 2026-11-23

- Added a claim check to both main workflows (issue #10).
  - The orchestrator checks each must-fix against the proposal or the cited file before the dossier.
  - A contradicted claim is dropped. An unverifiable claim is marked "unchecked".
  - Agreement between critics is a reason to check, not proof.
- Replaced the locked-score rule and the separate downgrade rule with one severity rule (issue #10).
  - A severity can rise freely.
  - A severity can drop only with named evidence written next to the score.
- Relabelled the SKILL workflow as sequential role-play (issue #11).
  - It runs in one shared context and is not independent.
  - Real independence needs the AGENT workflow and separate subagents.
- Added severity scores, a rewrite step and a final pass to the AGENT workflow (issue #11).
  - Each charter now requires a 1 to 5 severity score.
  - Each critic now answers: "Does the rewrite fix my objection, or only reframe it?"
  - Every dossier section now has a named input from both workflows.
- Left the skill review mode unchanged.

## 1.1.3 - 2026-11-23

- `claims.py` also resolves a bare file name under `skills/*/`, and reports ambiguous matches. Real must-fix citations in a plugin layout now quote the cited line.
- Critics now cite paths exactly as `git ls-files` prints them, for example `skills/<name>/SKILL.md:40`.

## 1.1.2 - 2026-11-23

- Adds the marketplace icon approved by Daniel (thedanielmay/agent-tools#2).

## 1.1.1 - 2026-11-23

- Marketplace file gains a description, so the full check passes again (thedanielmay/agent-tools#10).

## 1.1.0 - 2026-11-22

- Added skill review mode. Say "review this skill" or pass `--skill-review <path>` to review an agent skill with a fact pass, an optional field knowledge search, two or three critics and a verified dossier.
- Added a field knowledge stage. It finds up to two reputable outside skills on the subject, vets them, and gives the field expert their text as data. Nothing is installed or run.
- Added `scripts/claims.py`. It records each must-fix claim as held or dropped with the command that checked it, and refuses to write the verified file while one is unmarked.
- Added a planted-fault eval: a small made-up skill with five known faults, an answer key, and `evals/score.py`.
- Existing panel use is unchanged.

## 1.0.2 - 2026-11-22

- Removed the duplicate root SKILL.md. The skill now lives only in skills/expert-panel/SKILL.md.

## 1.0.1 - 2026-11-22

- Added the marketplace files: marketplace.json, LICENSE and CHANGELOG.md.
- Added license and metadata.version to both identical SKILL.md copies (root and skills/expert-panel/).
- Removed the email address from plugin.json and added the author url, homepage, repository and license.
- Added the plugin install line to README.md and removed the version number from its prose.
- Added .gitignore.

## 1.0.0

- initial publish.
