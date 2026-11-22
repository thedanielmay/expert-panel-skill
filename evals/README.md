# Eval for skill review mode

One fixture: `fixtures/planted-skill/SKILL.md`, a made-up skill with five planted faults. The answer key is `answer-key.json`. The review never reads it.

Pass: at least 4 of 5 planted faults found, and no invented must-fix.

## Run

1. Copy the fixture to a fresh folder outside this repo: `W=$(mktemp -d) && cp -R evals/fixtures/planted-skill "$W/" && git -C "$W/planted-skill" init -q`.
2. Start a session with this skill installed. Give it the prompt in `evals.json`, with `<WORK>` replaced by `$W`.
3. Let the mode run to `dossier.md`. Do not give it `answer-key.json`.
4. Score: `python3 evals/score.py <work folder>/dossier.md`. It exits 0 on a pass.
5. Read the invented must-fix list by hand. Each item is either a real extra fault (not invented) or a false claim (invented).

Limits: one fixture, one subject. It tests whether the mode finds what its designer planted. It is not a benchmark.
