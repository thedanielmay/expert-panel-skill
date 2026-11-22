"""Tests for evals/score.py. Run: python3 -m unittest discover -s tests"""
import subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCORE = ROOT / "evals/score.py"
KEY = ROOT / "evals/answer-key.json"

DOSSIER = """# Dossier
## Must-fix
1. Opposite orders on tense. Where: SKILL.md:31-34 and SKILL.md:48.
2. The git command fails. Where: SKILL.md:20.
3. Body is 524 lines, over the 500 lines limit.
4. A made-up fault about colours. Where: SKILL.md:300.
## Should-fix
- The save path is one person's home folder. Where: SKILL.md:41.
## Dropped claims
- Notes never mention breaking changes (dropped by mistake).
"""


def score(text, *extra):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "dossier.md"
        p.write_text(text)
        return subprocess.run([sys.executable, str(SCORE), str(p), "--key", str(KEY), *extra],
                              capture_output=True, text=True)


class TestScore(unittest.TestCase):
    def test_found_missed_invented(self):
        r = score(DOSSIER)
        out = r.stdout
        self.assertIn("found: contradiction, broken-command, over-length, owner-path", out)
        self.assertIn("missed: missing-rule", out)  # the only mention sits under Dropped claims
        self.assertIn("invented must-fix: 1", out)
        self.assertIn("SKILL.md:300", out)

    def test_pass_needs_four_found_and_no_invented(self):
        self.assertEqual(score(DOSSIER).returncode, 1)  # one invented
        ok = DOSSIER.replace("4. A made-up fault about colours. Where: SKILL.md:300.\n", "")
        self.assertEqual(score(ok).returncode, 0)  # 4 of 5, none invented

    def test_indented_sub_lines_belong_to_their_item(self):
        # the mode asks for each must-fix to carry its command and result on indented sub-lines
        text = ("## Must-fix\n1. The git command fails. SKILL.md:18\n   - Command: `git log --since-tag=v1.2.0`. Result: fatal.\n"
                "2. Home path. SKILL.md:40\n   - Command: `test -e /Users/alex/x`. Result: missing.\n"
                "3. Tense conflict. SKILL.md:33 and SKILL.md:48\n  - Command: `sed -n 33p SKILL.md`.\n"
                "4. No breaking changes rule. SKILL.md:25\n## Should-fix\n- Body over the length limit: 524 lines.\n")
        r = score(text)
        self.assertIn("invented must-fix: 0", r.stdout)
        self.assertEqual(r.returncode, 0)

    def test_three_found_fails(self):
        r = score("## Must-fix\n1. The git command fails. SKILL.md:18\n## Should-fix\n- Path. SKILL.md:40\n- Tense. SKILL.md:33\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("found: contradiction, broken-command, owner-path", r.stdout)

    def test_line_outside_tolerance_is_not_a_match(self):
        r = score("## Must-fix\n1. Wrong place. SKILL.md:25\n")
        self.assertIn("found: (none)", r.stdout)
        self.assertIn("invented must-fix: 1", r.stdout)


if __name__ == "__main__":
    unittest.main()
