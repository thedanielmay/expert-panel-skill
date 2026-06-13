# expert-panel-skill

A Claude Code skill that subjects any proposal to structured adversarial review by four domain experts, producing a decision dossier — not a verdict.

## Overview

`expert-panel` routes a proposal through either a skill or agent workflow, assembles a panel of four critics chosen along adversarial axes (not credential axes), runs structured independent and cross-challenge rounds, and outputs a **Decision Dossier**: must-fixes, should-fixes, unresolved objections, cross-panel tensions, and a steel-manned alternative.

The core principle: the goal is not consensus. An unresolved objection at the end is a valuable output. A verdict of "this cannot be salvaged in its current form" must be reachable.

**Version:** 1.0.0 (May 2026)  
**Category:** Decision & Review

---

## When to Use / Triggers

Claude activates this skill when the user asks to:

- Apply an **expert panel**, **three-expert panel**, **sceptical panel**, or **panel review** to a problem, design, plan, or decision
- **Challenge**, **interrogate**, **stress-test**, or **pressure-test** a proposal with domain experts

### Flags

| Flag | Effect |
|------|--------|
| `--skill` | Force the SKILL (sequential, in-context) workflow |
| `--agent` | Force the AGENT (parallel subagent dispatch) workflow |
| `--quick` | SKILL workflow, 2 rounds only |
| `--deep` | AGENT workflow with a second-pass dispatch enabled |

---

## What the Skill Does

### Stage 1 — Profile and Route

Before selecting any experts, the skill evaluates the proposal across four binary questions:

1. **Co-authorship risk** — Was it built with Claude/AI assistance?
2. **Stakes** — Is the decision reversible within a week?
3. **Blind-spot domain** — Does it touch security, concurrency, legal, compliance, or financial logic?
4. **External origin** — Did the proposal arrive from outside this conversation?

**Routing rule:**
- **SKILL workflow** — co-authorship=no AND stakes=low AND blind-spot=no
- **AGENT workflow** — co-authorship=yes OR stakes=high OR blind-spot=yes

The skill states the routing decision and a one-line rationale, then proceeds without waiting for user confirmation.

### Stage 2 — Expert Selection

Four experts are always used (three-person panels collapse into 2v1 consensus dynamics). Experts are selected across **adversarial axes**, not domain similarity:

1. **The beneficiary of failure** — whose position improves if the proposal fails
2. **The scarred practitioner** — someone who built something similar and watched it fail
3. **The outsider** — from a discipline entirely outside the proposal's frame
4. **The end-user reality** — representing the actual downstream consumer

### SKILL Workflow (sequential, 3 fixed rounds)

Used for low-stakes, externally-originated, non-blind-spot proposals.

- **Round 1 — Independent Critique:** Each expert critiques in strict isolation (no cross-referencing). Each pre-commits a severity score (1–5) that is locked — it can only be maintained or escalated.
- **Round 2 — Cross-Challenge:** Experts see each other's critiques. Each must identify one point of agreement and one point of disagreement. Severity scores cannot be softened without explicit named justification.
- **Round 3 — Post-Rewrite Stress Test:** Claude performs structured self-attack on the top three severity items, rewrites the proposal, and each expert does a final pass: "Does the rewrite address my objection, or just reframe it?"

Termination is fixed at three rounds. No loop. Unresolved objections go into the dossier verbatim.

### AGENT Workflow (parallel subagents)

Used for high-stakes, AI-co-authored, or blind-spot proposals.

1. The orchestrator writes four expert charters (proposal + adversarial axis + critique brief + 300-word cap + independence instruction)
2. All four subagents are dispatched in parallel in a single tool block
3. Critiques are collected; cross-cutting concerns and divergences are surfaced
4. (With `--deep`) A second-pass dispatch where each subagent sees the other three critiques
5. Orchestrator synthesises into the Decision Dossier

### Output — Decision Dossier

| Section | Contents |
|---------|----------|
| **Must-fix** (severity ≥ 4) | Specific failure scenario, expert(s) who raised it, failure condition |
| **Should-fix** (severity 2–3) | Same structure, lower urgency |
| **Unresolved objections** | Verbatim in the expert's voice — never paraphrased or softened |
| **Cross-panel tensions** | Where experts disagreed and what it implies — not resolved on their behalf |
| **Steel-man alternative** | Strongest case for not doing the proposal, argued as a competent advocate |

The dossier explicitly excludes: per-expert approval verdicts, satisfaction tickboxes, issue counts, or any rhetoric of consensus.

---

## What's Inside

```
SKILL.md                        # Root skill definition (loaded by Claude Code)
skills/
  expert-panel/
    SKILL.md                    # Canonical skill implementation
    metadata.json               # Version, category, abstract
```

The root `SKILL.md` and `skills/expert-panel/SKILL.md` are identical — the root copy is the entry point Claude Code reads; the `skills/` copy follows the standard skill-repo layout.

---

## Installation

Install via the Claude Code skill registry or by dropping the skill file into your Claude Code skills directory. The skill name is `expert-panel`.

> Exact installation steps depend on your Claude Code version and skill-loading configuration.

---

## Status

**v1.0.0** — Initial publish. Single commit. No open issues or PRs at time of writing.
