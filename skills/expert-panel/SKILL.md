---
name: expert-panel
description: Use when the user asks to apply an expert panel, three-expert panel, sceptical panel, or panel review to a problem, design, plan, or decision. Also use when the user says to challenge, interrogate, stress-test, or pressure-test a proposal with domain experts. Also use when the user asks to review an agent skill ("review this skill", "skill review", "panel review of a skill", "critique this SKILL.md", "is this skill any good"), or passes `--skill-review`.
license: MIT
metadata:
  version: "1.3.0"
---

# Expert Panel

## Core Principle

The goal is not consensus. The goal is to surface failure modes the proposal's author cannot see. An unresolved objection at the end is a valuable output, not a failure of the panel. A verdict of "this cannot be salvaged in its current form" must be reachable.

## Routing

If the request is a review of an agent skill, or `--skill-review <path>` is set, read `references/skill-review.md` and follow it. Skip Stages 1 and 2 of `references/panel.md`. The mode is unrelated to the SKILL workflow. It has its own claim verification in stage 4. Do not use the main-mode claim check in `references/panel.md`.

Otherwise, read `references/panel.md` in full before the panel run starts.

User overrides for a panel run:

- `--skill` — force SKILL workflow
- `--agent` — force AGENT workflow
- `--quick` — SKILL workflow, 2 rounds only
- `--deep` — AGENT workflow with second pass enabled

## Severity rule

Use this rule in both workflows and in the dossier.

- A severity can rise freely at any stage. Raise it when new evidence makes the failure more likely or more serious.
- A severity can drop only with named evidence: what was checked and what it showed. Write that evidence next to the score.
- A score with no named evidence beside it does not drop. Tone and politeness are not evidence.

## References

- `references/panel.md`: read in full before a panel run starts.
- `references/skill-review.md`: read when the request is a review of an agent skill or `--skill-review <path>` is set.
- `references/skill-review-briefs/`: briefs for the skill review stages, filled in and handed to subagents as `skill-review.md` directs.
