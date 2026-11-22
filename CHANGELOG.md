# Changelog

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
