# tests/test_integration.py
import json
import os
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D1 = os.path.join(ROOT, "data", "processed", "dataset1")


class TestDataset1Build(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["python3", "prepare_dataset1.py"], cwd=ROOT, check=True)

    def test_five_series_files_exist(self):
        for slug in ["urea", "dap", "tsp", "phosphate-rock", "mop"]:
            self.assertTrue(os.path.exists(os.path.join(D1, f"{slug}.json")), slug)

    def test_series_are_gapless_chronological_finite(self):
        for slug in ["urea", "dap", "tsp", "phosphate-rock", "mop"]:
            with open(os.path.join(D1, f"{slug}.json")) as fh:
                series = json.load(fh)
            keys = list(series.keys())
            self.assertEqual(keys, sorted(keys), f"{slug} not chronological")
            # 1996-04 .. 2026-03 inclusive = 360 months, no gaps
            self.assertEqual(len(keys), 360, f"{slug} wrong length")
            for v in series.values():
                self.assertTrue(isinstance(v, float))

    def test_phosphate_rock_gap_was_filled(self):
        with open(os.path.join(D1, "phosphate-rock.json")) as fh:
            series = json.load(fh)
        self.assertIn("2023-11-01", series)

    def test_quality_csv_flags_phosphate_rock(self):
        import csv
        with open(os.path.join(D1, "dataset1_quality.csv")) as fh:
            rows = {r["product"]: r for r in csv.DictReader(fh)}
        self.assertEqual(rows["Phosphate rock"]["data_quality"], "review")
        self.assertIn("stale_flat_tail", rows["Phosphate rock"]["flags"])
