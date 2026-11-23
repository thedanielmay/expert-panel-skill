"""Tests for skills/expert-panel/scripts/claims.py. Run: python3 -m unittest discover -s tests"""
import importlib.util, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills/expert-panel/scripts/claims.py"

CRITIC_A = """# x: field
Prose that mentions 5 | a:1 | not a claim, outside the block.
```claims
5 | SKILL.md:2 | the command on this line fails
2 | SKILL.md:3 | a small wording problem
```
"""
CRITIC_B = """```claims
4 | SKILL.md:99 | a line past the end of the file
4 | - | a rule the field expects is missing
```
"""


def run(work, repo, *args):
    return subprocess.run([sys.executable, str(SCRIPT), "--dir", str(work), "--repo", str(repo), *args],
                          capture_output=True, text=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name) / "work"
        self.repo = Path(self.tmp.name) / "repo"
        self.work.mkdir(); self.repo.mkdir()
        (self.repo / "SKILL.md").write_text("line one\nrun the bad command\nthird line\n")
        (self.work / "critic-field.md").write_text(CRITIC_A)
        (self.work / "critic-against.md").write_text(CRITIC_B)

    def tearDown(self):
        self.tmp.cleanup()

    def claims(self):
        return json.loads((self.work / "claims.json").read_text())

    def extract(self):
        r = run(self.work, self.repo, "extract")
        self.assertEqual(r.returncode, 0, r.stderr)

    def must_ids(self):
        return [c["id"] for c in self.claims() if c["severity"] >= 4]


class TestExtract(Base):
    def test_parses_both_files_and_ignores_prose(self):
        self.extract()
        self.assertEqual(sorted(c["severity"] for c in self.claims()), [2, 4, 4, 5])

    def test_malformed_line_is_rejected_with_file_and_line(self):
        (self.work / "critic-field.md").write_text("```claims\nsevere | SKILL.md:2 | x\n```\n")
        r = run(self.work, self.repo, "extract")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("critic-field.md:2", r.stderr)

    def test_rerun_takes_a_raised_severity(self):
        # a critic who raises a should-fix to must-fix makes it a must-fix on re-extract
        self.extract()
        (self.work / "critic-field.md").write_text(CRITIC_A.replace("\n2 |", "\n5 |", 1))
        self.extract()
        self.assertEqual(sorted(c["severity"] for c in self.claims()), [4, 4, 5, 5])

    def test_rerun_keeps_marks(self):
        self.extract()
        cid = self.must_ids()[0]
        run(self.work, self.repo, "mark", cid, "held", "--cmd", "sed -n 2p SKILL.md", "--note", "confirmed")
        self.extract()
        c = next(c for c in self.claims() if c["id"] == cid)
        self.assertEqual(c["status"], "held")
        self.assertEqual(c["cmd"], "sed -n 2p SKILL.md")


class TestList(Base):
    def test_shows_quoted_line_and_unmarked(self):
        self.extract()
        out = run(self.work, self.repo, "list").stdout
        self.assertIn("run the bad command", out)
        self.assertIn("unmarked", out)
        self.assertNotIn("a small wording problem", out)  # severity 2 is not listed

    def test_missing_line_is_unresolvable_and_no_line_is_labelled(self):
        self.extract()
        out = run(self.work, self.repo, "list").stdout
        self.assertIn("unresolvable", out)
        self.assertIn("no line cited", out)


class TestMark(Base):
    def setUp(self):
        super().setUp()
        self.extract()
        self.cid = self.must_ids()[0]

    def test_empty_cmd_refused(self):
        r = run(self.work, self.repo, "mark", self.cid, "held", "--cmd", " ", "--note", "x")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.claims()[0]["status"], "unmarked")

    def test_dropped_without_note_refused(self):
        r = run(self.work, self.repo, "mark", self.cid, "dropped", "--cmd", "true")
        self.assertNotEqual(r.returncode, 0)

    def test_unknown_id_refused(self):
        r = run(self.work, self.repo, "mark", "c999", "held", "--cmd", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("c999", r.stderr)


class TestDossierNoExtract(Base):
    def test_refuses_when_extract_never_ran(self):
        r = run(self.work, self.repo, "dossier")
        self.assertEqual(r.returncode, 2)
        self.assertIn("extract", r.stderr)
        self.assertFalse((self.work / "verified.md").exists())


class TestDossier(Base):
    def setUp(self):
        super().setUp()
        self.extract()

    def mark_all(self, status_for=lambda i: "held"):
        for i, cid in enumerate(self.must_ids()):
            run(self.work, self.repo, "mark", cid, status_for(i), "--cmd", "sed -n 2p SKILL.md", "--note", "checked")

    def test_refuses_with_exit_2_and_names_ids_and_writes_nothing(self):
        r = run(self.work, self.repo, "dossier")
        self.assertEqual(r.returncode, 2)
        for cid in self.must_ids():
            self.assertIn(cid, r.stderr)
        self.assertFalse((self.work / "verified.md").exists())

    def test_one_unmarked_still_refuses(self):
        ids = self.must_ids()
        for cid in ids[:-1]:
            run(self.work, self.repo, "mark", cid, "held", "--cmd", "true")
        r = run(self.work, self.repo, "dossier")
        self.assertEqual(r.returncode, 2)
        self.assertIn(ids[-1], r.stderr)
        self.assertNotIn(ids[0], r.stderr)

    def test_unmarked_should_fix_does_not_block(self):
        self.mark_all()
        self.assertEqual(run(self.work, self.repo, "dossier").returncode, 0)
        self.assertTrue((self.work / "verified.md").exists())

    def test_counts_held_and_dropped_and_shows_command(self):
        self.mark_all(lambda i: "held" if i == 0 else "dropped")
        self.assertEqual(run(self.work, self.repo, "dossier").returncode, 0)
        text = (self.work / "verified.md").read_text()
        self.assertIn("Held: 1", text)
        self.assertIn("Dropped: 2", text)
        self.assertIn("sed -n 2p SKILL.md", text)


class TestPluginLayout(Base):
    """A plugin repo keeps SKILL.md under skills/<name>/, not at the repo root."""
    def setUp(self):
        super().setUp()
        (self.repo / "SKILL.md").unlink()
        foo = self.repo / "skills" / "foo"
        foo.mkdir(parents=True)
        (foo / "SKILL.md").write_text("line one\nrun the foo command\nthird line\n")
        for f in self.work.glob("critic-*.md"):
            f.unlink()

    def listed(self, loc):
        (self.work / "critic-field.md").write_text(f"```claims\n5 | {loc} | a plugin layout claim\n```\n")
        self.extract()
        return run(self.work, self.repo, "list").stdout

    def test_bare_name_resolves_under_the_single_skill(self):
        out = self.listed("SKILL.md:2")
        self.assertIn("run the foo command", out)
        self.assertNotIn("unresolvable", out)

    def test_bare_name_in_two_skills_is_ambiguous(self):
        bar = self.repo / "skills" / "bar"
        bar.mkdir(parents=True)
        (bar / "SKILL.md").write_text("line one\nrun the bar command\nthird line\n")
        out = self.listed("SKILL.md:2")
        self.assertIn("unresolvable: ambiguous", out)
        self.assertIn("skills/bar/SKILL.md", out)
        self.assertIn("skills/foo/SKILL.md", out)

    def test_bare_name_in_no_skill_stays_unresolvable(self):
        out = self.listed("missing.md:2")
        self.assertIn("unresolvable", out)
        self.assertNotIn("ambiguous", out)

    def test_root_path_still_wins_over_skills_copy(self):
        (self.repo / "SKILL.md").write_text("line one\nrun the root command\nthird line\n")
        out = self.listed("SKILL.md:2")
        self.assertIn("run the root command", out)
        self.assertNotIn("run the foo command", out)


class TestNoLeaks(unittest.TestCase):
    """The skill ships to a marketplace: no owner names, home paths or emails in new files."""
    def test_new_files_are_clean(self):
        import re
        # built from pieces so this file holds none of the strings it hunts
        bad = re.compile("/Us" + "ers/|thedaniel" + "may|standing-" + r"orders|[\w.+-]+@[\w-]+\.[\w.]+")
        files = [p for d in ("skills/expert-panel/references", "skills/expert-panel/scripts", "evals")
                 for p in (ROOT / d).rglob("*") if p.is_file() and "fixtures" not in p.parts
                 and "__pycache__" not in p.parts and p.name != "answer-key.json"]
        files.append(ROOT / "skills/expert-panel/SKILL.md")
        hits = [f"{p.relative_to(ROOT)}:{n}" for p in files
                for n, line in enumerate(p.read_text().splitlines(), 1) if bad.search(line)]
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
