#!/usr/bin/env python3
"""Claims file for skill review: extract claims from critic files, list must-fixes,
record held/dropped marks with the command run, and refuse the dossier while a must-fix is unmarked.

  claims.py [--dir WORK] [--repo TARGET] extract | list | mark ID held|dropped --cmd C [--note N] | dossier

A critic ends its file with a fenced block (info string `claims`), one claim per line:
  severity | file:line | one-sentence claim      (file:line is `-` when the claim is about something absent)
A must-fix is severity 4 or 5. The script proves a mark was recorded with a command.
It does not prove the command was a good test.
"""
import argparse, json, re, sys
from pathlib import Path

MUST = 4


def die(msg, code=1):
    print(f"claims: {msg}", file=sys.stderr)
    sys.exit(code)


def load(work):
    p = work / "claims.json"
    return json.loads(p.read_text()) if p.exists() else []


def save(work, claims):
    (work / "claims.json").write_text(json.dumps(claims, indent=2) + "\n")


def extract(work):
    old = {(c["loc"], c["claim"]): c for c in load(work)}
    out, nxt = [], 1 + max([int(c["id"][1:]) for c in old.values()] or [0])
    for f in sorted(work.glob("critic-*.md")):
        inside = False
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if line.strip().startswith("```"):
                inside = line.strip() == "```claims" and not inside
                continue
            if not inside or not line.strip():
                continue
            parts = [x.strip() for x in line.split("|", 2)]
            if len(parts) != 3 or not re.fullmatch(r"[1-5]", parts[0]) or not parts[2] \
                    or not re.fullmatch(r"-|[^\s:]+:\d+", parts[1]):
                die(f"{f.name}:{n}: expected 'severity 1-5 | file:line or - | claim', got: {line!r}")
            key = (parts[1], parts[2])
            c = old.get(key)
            if c is None:
                c = {"id": f"c{nxt}", "severity": int(parts[0]), "loc": parts[1], "claim": parts[2],
                     "status": "unmarked", "cmd": "", "note": ""}
                nxt += 1
            c["source"] = f.name
            out.append(c)
    save(work, out)
    print(f"{len(out)} claims, {sum(c['severity'] >= MUST for c in out)} must-fix")


def quote(repo, loc):
    if loc == "-":
        return "(no line cited: the claim is about something absent)"
    name, n = loc.rsplit(":", 1)
    try:
        lines = (repo / name).read_text().splitlines()
        return lines[int(n) - 1].strip() if int(n) >= 1 else "unresolvable"
    except (OSError, IndexError):
        return "unresolvable: file or line does not exist"


def must(claims):
    return [c for c in claims if c["severity"] >= MUST]


def list_(work, repo):
    for c in must(load(work)):
        print(f"{c['id']}  [{c['severity']}]  {c['loc']}  status: {c['status']}")
        print(f"    claim: {c['claim']}")
        print(f"    line:  {quote(repo, c['loc'])}")
        if c["status"] != "unmarked":
            print(f"    cmd:   {c['cmd']}")


def mark(work, cid, status, run, note):
    claims = load(work)
    c = next((c for c in claims if c["id"] == cid), None)
    if c is None:
        die(f"unknown claim id {cid}")
    if not run.strip():
        die("a mark needs a non-empty --cmd: the command you ran to check the claim")
    if status == "dropped" and not note.strip():
        die("dropped needs --note giving the reason")
    c.update(status=status, cmd=run.strip(), note=note.strip())
    save(work, claims)
    print(f"{cid} {status}")


def dossier(work):
    claims = load(work)
    open_ids = [c["id"] for c in must(claims) if c["status"] == "unmarked"]
    if open_ids:
        die("refusing: must-fix claims still unmarked: " + ", ".join(open_ids), 2)
    held = [c for c in claims if c["status"] == "held"]
    dropped = [c for c in claims if c["status"] == "dropped"]
    out = ["# Verified claims", "", f"Held: {len(held)}", f"Dropped: {len(dropped)}",
           f"Should-fix claims not marked: {sum(c['status'] == 'unmarked' for c in claims)}", "", "## Held", ""]
    for c in held:
        out += [f"- {c['id']} [{c['severity']}] {c['loc']}: {c['claim']}",
                f"  - command: `{c['cmd']}`", f"  - result: {c['note'] or '(none)'}"]
    out += ["", "## Dropped", ""]
    out += [f"- {c['id']} [{c['severity']}] {c['loc']}: {c['claim']} (reason: {c['note']})" for c in dropped]
    (work / "verified.md").write_text("\n".join(out) + "\n")
    print(f"wrote {work / 'verified.md'}: {len(held)} held, {len(dropped)} dropped")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".", help="work folder holding critic-*.md (default .)")
    ap.add_argument("--repo", default=".", help="the reviewed repo, used to quote cited lines (default .)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("extract"); sub.add_parser("list"); sub.add_parser("dossier")
    m = sub.add_parser("mark")
    m.add_argument("id"); m.add_argument("status", choices=["held", "dropped"])
    m.add_argument("--cmd", dest="run", default=""); m.add_argument("--note", default="")
    a = ap.parse_args()
    work, repo = Path(a.dir), Path(a.repo)
    if a.cmd == "extract":
        extract(work)
    elif a.cmd == "list":
        list_(work, repo)
    elif a.cmd == "mark":
        mark(work, a.id, a.status, a.run, a.note)
    else:
        dossier(work)


if __name__ == "__main__":
    main()
