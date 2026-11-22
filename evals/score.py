#!/usr/bin/env python3
"""Compare a skill-review dossier with the answer key: found, missed, invented.

  python3 evals/score.py DOSSIER.md [--key evals/answer-key.json]

found    = planted faults the dossier mentions outside its Dropped section, by a SKILL.md:line reference
           within the key's tolerance, or by one of the fault's phrases.
invented = items in the Must-fix section that match no planted fault. A person reads each one:
           a real extra fault is not invented, a false claim is.
Pass     = at least 4 of 5 found and no invented must-fix. Exit 0 on pass, 1 otherwise.
"""
import argparse, json, re, sys
from pathlib import Path

REF = re.compile(r"SKILL\.md:(\d+)(?:-(\d+))?")


def sections(text):
    """[(heading, body)] split on level-2 headings."""
    parts = re.split(r"^## +(.*)$", text, flags=re.M)
    return [(parts[i].strip().lower(), parts[i + 1]) for i in range(1, len(parts), 2)]


def hits(fault, text, tol):
    for m in REF.finditer(text):
        lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
        if any(lo - tol <= n <= hi + tol for n in fault["lines"]):
            return True
    low = text.lower()
    return any(p in low for p in fault["phrases"])


def items(body):
    out = []
    for line in body.splitlines():
        if re.match(r"\s{0,3}(?:[-*]|\d+[.)])\s", line):
            out.append(line)
        elif out and line.strip():
            out[-1] += " " + line.strip()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier")
    ap.add_argument("--key", default=str(Path(__file__).with_name("answer-key.json")))
    a = ap.parse_args()
    key = json.loads(Path(a.key).read_text())
    tol, faults = key["tolerance_lines"], key["faults"]
    kept = [(h, b) for h, b in sections(Path(a.dossier).read_text()) if "dropped" not in h]
    text = "\n".join(b for _, b in kept)
    found = [f["id"] for f in faults if hits(f, text, tol)]
    missed = [f["id"] for f in faults if f["id"] not in found]
    invented = [i.strip() for h, b in kept if "must" in h and "fix" in h
                for i in items(b) if not any(hits(f, i, tol) for f in faults)]
    print(f"found: {', '.join(found) or '(none)'}")
    print(f"missed: {', '.join(missed) or '(none)'}")
    print(f"invented must-fix: {len(invented)}")
    for i in invented:
        print(f"  {i}")
    ok = len(found) >= 4 and not invented
    print(f"{len(found)} of {len(faults)} found: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
