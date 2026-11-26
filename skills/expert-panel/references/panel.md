# Expert Panel

Subject a proposal to structured adversarial review by four domain experts. Produce a decision dossier: must-fixes, should-fixes, unresolved objections, cross-panel tensions, and a steel-manned alternative.

## Stage 1 — Profile and Route

Before selecting experts or running any review, answer these four binary questions about the proposal:

1. **Co-authorship risk** — Was this proposal built with Claude in this conversation, or with substantial AI assistance? (yes = agent risk)
2. **Stakes** — Is the decision reversible within a week? (no = high stakes)
3. **Blind-spot domain** — Does this involve security, concurrency, legal, compliance, or financial logic? (yes = blind-spot risk)
4. **External origin** — Did the proposal arrive from outside this conversation (colleague, vendor, the user's own independent work)? (yes = lower contamination risk)

**Routing rule:**

- Route to **SKILL workflow** if: co-authorship = no AND stakes = low AND blind-spot = no
- Route to **AGENT workflow** if: co-authorship = yes OR stakes = high OR blind-spot = yes

**User overrides:** the four flags are listed in `SKILL.md` under Routing.

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

### Round 1: Sequential role-play (not independent)

Experts critique in sequence, in their own voice, in one shared context. The orchestrator plays each role in turn. Later roles see earlier critiques in the context, even when told not to use them. This is not independent review. Real independence needs the AGENT workflow, where each critic runs as a separate subagent with no shared context.

Give each role this instruction before it speaks: do not reference earlier experts' points. Re-derive the objection from the proposal itself. Treat this as a role-play instruction, not a guarantee of independence.

Frame each expert's turn explicitly:

> "Expert 2 speaks now. Do not reference Expert 1's critique. Re-derive the objection from the proposal."

The beneficiary-of-failure expert also states the strongest case for not doing the proposal. That critique is the input for the steel-man alternative.

**Pre-commit severity.** Before the proposal author defends, each expert rates their top objection on a 1 to 5 severity scale. Write the scores down. Apply the Severity rule to every later change.

### Round 2 — Cross-Challenge

Experts now see each other's critiques. Each expert must do all three:

1. Identify one point from another expert they **agree with**, and state why it changes their view.
2. Identify one point from another expert they **disagree with**. (Cross-panel tension is mandatory, not optional. If every expert agrees with every other expert, the panel has collapsed — re-run Round 1 with sharper adversarial axes.)
3. Keep or raise the severity score. To lower it, apply the Severity rule and write the named evidence next to the score.

### Round 3 — Post-Rewrite Stress Test

The proposal author (Claude) now does structured self-attack:

1. List the **three weaknesses with the highest current severity scores**.
2. For each, state the specific failure scenario in concrete terms: "this fails when X happens because Y."
3. Rewrite the proposal to fix those weaknesses.
4. Each expert does one final pass on the rewrite, answering one question: **"Does the rewrite fix my objection, or only reframe it?"** Record the answer verbatim. Any "only reframe it" answer goes into Unresolved objections.

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
- A 1 to 5 severity score for the top objection, with one line naming the evidence behind it
- The explicit instruction: **"You have not seen any other expert's critique. Derive your objections independently."**

Make one of the four charters the case against. It argues the strongest case for not doing the proposal. That critique is the input for the steel-man alternative.

### Step 2 — Dispatch in parallel

Launch all 4 subagents in a single tool block, in parallel. Each runs independently with no shared context.

### Step 3 — Collect and surface tensions

Collect the 4 critiques. Identify:

- **Cross-cutting concerns**: where experts landed on the same issue. Agreement is a reason to check the claim, not proof. Apply the claim check before the dossier.
- **Divergences** — where experts attacked different parts of the proposal or reached opposite conclusions. Surface these as cross-panel tensions; do not resolve them prematurely.

### Step 4 (optional, --deep only) — Second-pass dispatch

Each subagent now sees the other three critiques. Each answers:

- "What changed your position after reading the others?"
- "What did they miss that you caught?"

Dispatch in parallel again. Collect. Re-surface tensions.

### Step 5: Rewrite and final pass

1. The orchestrator rewrites the proposal to fix the objections with the highest severity scores.
2. Send each critic the rewrite and their own original critique. Dispatch in parallel again.
3. Each critic answers one question: **"Does the rewrite fix my objection, or only reframe it?"** State the severity score after the rewrite. Apply the Severity rule to any change.
4. Record each answer verbatim. Any "only reframe it" answer goes into Unresolved objections.

### Step 6: Orchestrator synthesises

Move to the Decision Dossier output.

## Claim check before the dossier

Use this in both workflows. Check each must-fix (severity 4 or 5) before it enters the dossier. Check the factual claim against the proposal text or the cited file.

- Agreement between critics is a reason to check, not proof. Two critics can repeat the same wrong claim.
- Check a claim about a number, a command or a count by running the command or opening the cited file. Do not ask the critic to reread it. Every figure comes with the command that produced it.
- Record one result for each must-fix:
  - **Held**: the evidence confirms the claim. Write what was checked and what it showed next to the score.
  - **Dropped**: the evidence contradicts the claim. Remove it from Must-fix and Should-fix. Keep one line under Dropped claims with the reason.
  - **Unchecked**: the evidence cannot be reached. Keep the claim in its severity section. Mark it "unchecked" next to the score. Say what was not reachable. Do not present it as verified.
- The named evidence written for a drop is also the evidence required by the Severity rule.

## Dossier inputs

Both workflows produce an input for every dossier section.

| Dossier section | SKILL workflow | AGENT workflow |
|---|---|---|
| Must-fix | Round 1 scores, Round 2 changes, claim check | Charter scores, Step 5 changes, claim check |
| Should-fix | Round 1 scores, Round 2 changes, claim check | Charter scores, Step 5 changes, claim check |
| Unresolved objections | Round 3 final-pass answers | Step 5 final-pass answers |
| Cross-panel tensions | Round 2 disagreements | Step 3 divergences, Step 4 second pass (with `--deep`) |
| Steel-man alternative | Round 1 case-against critique | Case-against charter, Step 5 final pass |
| Dropped claims | Claim check | Claim check |

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

### Dropped claims

One line per dropped must-fix, with the reason and the evidence that contradicted it. Unchecked claims stay in their severity section with the "unchecked" label.

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
- **Sequential in Round 1** (not independent): experts speak in turn in one shared context and set aside earlier critiques until Round 2
- **Permitted to conclude the proposal cannot be salvaged in its current form** — this verdict must be reachable and stated plainly when warranted

### Experts MUST NOT be

- **Agreeable** — "looks good" is failure
- **Deferential** — confidence from the proposal author is not evidence
- **Unanimous by default** — if all four agree on everything, the panel has failed structurally
- **Constrained to be constructive** — a verdict of "this is the wrong proposal" is a legitimate and useful output
