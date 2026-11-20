import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import assess


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "synthetic-evidence.json"


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(SAMPLE.read_text(encoding="utf-8"))
        directory = TemporaryDirectory(dir=ROOT)
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "evidence.json"

    def load(self, data):
        self.path.write_text(json.dumps(data), encoding="utf-8")
        return assess.load_evidence(self.path)

    def run_cli(self, path):
        return subprocess.run(
            [sys.executable, str(ROOT / "assess.py"), str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_sample_cli_matches_checked_in_report(self):
        result = self.run_cli(SAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        expected = (ROOT / "examples" / "synthetic-report.md").read_text(encoding="utf-8")
        self.assertEqual(result.stdout, expected)
        self.assertIn("3 exposure findings", result.stdout)
        self.assertIn("2 high, 1 medium", result.stdout)
        self.assertIn("5 of 9", result.stdout)
        self.assertEqual(result.stdout.count("### Synthetic finding"), 3)
        self.assertNotIn("Evidence reference** — `DEMO-02`", result.stdout)

    def test_out_of_scope_cli_rejects_entire_input(self):
        self.data["observations"][-1]["asset"] = "outside-scope"
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        result = self.run_cli(self.path)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("outside the approved scope", result.stderr)

    def test_present_absent_and_missing_are_distinct(self):
        self.data["observations"] = [self.data["observations"][1]]
        report = assess.render_report(self.load(self.data))
        self.assertIn("0 exposure findings", report)
        self.assertIn("1 of 9", report)
        self.assertIn("`DEMO-02` | Absent", report)
        self.assertIn("No evidence supplied", report)

    def test_empty_evidence_reports_no_coverage(self):
        self.data["observations"] = []
        report = assess.render_report(self.load(self.data))
        self.assertIn("0 of 9", report)
        self.assertNotIn("### Synthetic finding", report)

    def test_non_synthetic_rendering_omits_demo_markers(self):
        self.data["synthetic"] = False
        report = assess.render_report(self.load(self.data))
        self.assertIn("### Finding 1", report)
        self.assertNotIn("Synthetic", report)
        self.assertIn("reported", report)

    def test_invalid_schema_and_duplicates_are_rejected(self):
        first, second = self.data["observations"][:2]
        cases = (
            {"synthetic": "true"},
            {"approved_assets": []},
            {"approved_assets": [f"asset-{i}" for i in range(6)]},
            {"approved_assets": ["duplicate", "duplicate"]},
            {"approved_assets": ["unsafe|asset"]},
            {"observations": {}},
            {"observations": [{**first, "present": 1}]},
            {"observations": [{**first, "check": "unknown"}]},
            {"observations": [{**first, "unrecognized": True}]},
            {"observations": [{**first, "id": "bad`id"}]},
            {"observations": [first, {**second, "id": first["id"]}]},
            {"observations": [first, {**first, "id": "DEMO-99", "present": False}]},
        )
        for update in cases:
            with self.subTest(update=update):
                data = copy.deepcopy(self.data)
                data.update(update)
                with self.assertRaises(ValueError):
                    self.load(data)

    def test_malformed_missing_and_duplicate_key_inputs_fail(self):
        for content in ("{", '{"synthetic": true, "synthetic": false}'):
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                result = self.run_cli(self.path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("Assessment rejected", result.stderr)
        result = self.run_cli(self.path.with_name("missing.json"))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Assessment rejected", result.stderr)
