---
name: expert-panel
description: Use when the user asks to apply an expert panel, three-expert panel, sceptical panel, or panel review to a problem, design, plan, or decision. Also use when the user says to challenge, interrogate, stress-test, or pressure-test a proposal with domain experts. Also use when the user asks to review an agent skill ("review this skill", "skill review", "panel review of a skill", "critique this SKILL.md", "is this skill any good"), or passes `--skill-review`.
license: MIT
metadata:
  version: "1.1.3"
---

# Expert Panel

Subject a proposal to structured adversarial review by four domain experts. Produce a decision dossier: must-fixes, should-fixes, unresolved objections, cross-panel tensions, and a steel-manned alternative.

## Core Principle

The goal is not consensus. The goal is to surface failure modes the proposal's author cannot see. An unresolved objection at the end is a valuable output, not a failure of the panel. A verdict of "this cannot be salvaged in its current form" must be reachable.

## Skill review mode

If the request is a review of an agent skill, or `--skill-review <path>` is set, read `references/skill-review.md` and follow it.
Skip Stages 1 and 2 below. The mode is unrelated to the SKILL workflow.
Otherwise ignore this section.

## Stage 1 — Profile and Route

Before selecting experts or running any review, answer these four binary questions about the proposal:

1. **Co-authorship risk** — Was this proposal built with Claude in this conversation, or with substantial AI assistance? (yes = agent risk)
2. **Stakes** — Is the decision reversible within a week? (no = high stakes)
3. **Blind-spot domain** — Does this involve security, concurrency, legal, compliance, or financial logic? (yes = blind-spot risk)
4. **External origin** — Did the proposal arrive from outside this conversation (colleague, vendor, the user's own independent work)? (yes = lower contamination risk)

**Routing rule:**

- Route to **SKILL workflow** if: co-authorship = no AND stakes = low AND blind-spot = no
- Route to **AGENT workflow** if: co-authorship = yes OR stakes = high OR blind-spot = yes

**User overrides:**

- `--skill` — force SKILL workflow
- `--agent` — force AGENT workflow
- `--quick` — SKILL workflow, 2 rounds only
- `--deep` — AGENT workflow with second pass enabled

State the routing decision and a one-line rationale, then proceed. Do not ask the user to confirm the route.

```
Route: AGENT (co-authorship=yes, stakes=high). Dispatching 4 parallel critics.
```

## Stage 2 — Expert Selection

**Default: 4 experts.** Three-person panels collapse into 2v1 dynamics that converge on consensus. Four preserves cross-tension.

Select across **adversarial axes**, not domain credibility. The panel must include at least one of each:

1. **The beneficiary of failure** — someone whose position improves if this proposal fails (competing vendor, internal rival team, the person who proposed the alternative)
2. **The scarred practitioner** — someone who has built something structurally similar and watched it fail in production
3. **The outsider** — someone from a discipline outside the proposal's frame (an anthropologist on a technical proposal, an operations engineer on a UX proposal, a litigator on an engineering proposal)
4. **The end-user reality** — someone who represents the actual user, customer, or downstream consumer — not the builder's mental model of them

Do not select four engineers for an engineering proposal. Credentialed-same-domain panels converge fastest.

State the panel — name, role, adversarial axis, what they will specifically attack — and proceed. No confirmation gate. The user can interrupt if they want different experts.

## SKILL Workflow — 3 fixed rounds, no loop

Use when routing decision selects SKILL.

### Round 1 — Independent Critique (strict isolation)

Each expert critiques in sequence, in their own voice. **Strict constraint:** Expert 2 must not reference Expert 1's points. Expert 3 must not reference Experts 1 or 2. Expert 4 must not reference any prior expert. Each must re-derive their objections independently, as if they have not heard the others.

Frame each expert's turn explicitly:

> "Expert 2 speaks now, without reference to Expert 1's critique. Independent derivation only."

**Pre-commit severity.** Before the proposal author defends, each expert rates their top objection on a 1–5 severity scale. Write the scores down. These are **locked** — they cannot be retroactively softened in later rounds. They can only be maintained or escalated.

### Round 2 — Cross-Challenge

Experts now see each other's critiques. Each expert must do all three:

1. Identify one point from another expert they **agree with**, and state why it changes their view.
2. Identify one point from another expert they **disagree with**. (Cross-panel tension is mandatory, not optional. If every expert agrees with every other expert, the panel has collapsed — re-run Round 1 with sharper adversarial axes.)
3. Maintain or escalate their pre-committed severity score. Downgrading requires explicit, named justification ("Expert 3's point about X actually resolves my Y concern because Z") — never a softening on tone alone.

### Round 3 — Post-Rewrite Stress Test

The proposal author (Claude) now does structured self-attack:

1. List the **three weaknesses with the highest pre-committed severity scores**.
2. For each, state the specific failure scenario in concrete terms: "this fails when X happens because Y."
3. Rewrite the proposal to fix those weaknesses.
4. Each expert does one final pass on the rewrite, answering one question: **"Does the rewrite address my pre-committed objection, or does it just reframe it?"**

Experts are permitted — and encouraged — to end Round 3 with an unresolved objection. That is a valid and high-value output.

**Termination is fixed.** Three rounds, then synthesise. No loop. No "unanimous satisfaction." If objections remain unresolved, they go into the dossier verbatim.

## AGENT Workflow — parallel subagent dispatch

Use when routing decision selects AGENT, or when `--deep` is set.

### Step 1 — Define charters

The orchestrator (Claude) writes 4 expert charters. Each charter contains:

- The proposal in full
- The expert's adversarial axis (from Stage 2)
- A specific critique brief ("attack this from the perspective of …")
- A 300-word cap on the critique
- The explicit instruction: **"You have not seen any other expert's critique. Derive your objections independently."**

### Step 2 — Dispatch in parallel

Launch all 4 subagents in a single tool block, in parallel. Each runs independently with no shared context.

### Step 3 — Collect and surface tensions

Collect the 4 critiques. Identify:

- **Cross-cutting concerns** — where experts independently landed on the same issue. This is high-signal. The objection is structural to the proposal, not stylistic.
- **Divergences** — where experts attacked different parts of the proposal or reached opposite conclusions. Surface these as cross-panel tensions; do not resolve them prematurely.

### Step 4 (optional, --deep only) — Second-pass dispatch

Each subagent now sees the other three critiques. Each answers:

- "What changed your position after reading the others?"
- "What did they miss that you caught?"

Dispatch in parallel again. Collect. Re-surface tensions.

### Step 5 — Orchestrator synthesises

Move to the Decision Dossier output.

## Output Format — Decision Dossier

The output is a dossier, not a verdict. Sections:

### Must-fix (severity ≥ 4)

For each: the specific failure scenario, the expert(s) who raised it, and the concrete condition under which the proposal fails.

### Should-fix (severity 2–3)

Same structure, lower urgency.

### Unresolved objections

Objections that the rewrite did not address. Preserved **verbatim** in the expert's voice. Do not paraphrase, soften, or summarise away. This is the highest-value section of the dossier.

### Cross-panel tensions

Where experts disagreed with each other. State both positions and what the disagreement implies for the decision — do not resolve it on the experts' behalf.

### Steel-man alternative

The strongest case for **not doing this proposal**, or doing the opposite. Argued as if by a competent advocate, not strawmanned. One paragraph minimum.

### Do not include

- Per-expert approval verdicts ("Karan: approved")
- Satisfaction tickboxes
- Counts of issues raised vs resolved
- Any rhetoric of consensus

These are performance metrics for theatre, not adversarial review.

## Expert Behaviour Rules

### Experts MUST be

- **Sceptical by default** — every claim is suspect until evidenced
- **Relentless** — they do not stop at "good enough"
- **Specific** — challenges cite exact scenarios, thresholds, conditions, line numbers, edge cases. Never vague.
- **Independent in Round 1** — no reference to other experts' points until Round 2
- **Permitted to conclude the proposal cannot be salvaged in its current form** — this verdict must be reachable and stated plainly when warranted

### Experts MUST NOT be

- **Agreeable** — "looks good" is failure
- **Deferential** — confidence from the proposal author is not evidence
- **Unanimous by default** — if all four agree on everything, the panel has failed structurally
- **Constrained to be constructive** — a verdict of "this is the wrong proposal" is a legitimate and useful output
