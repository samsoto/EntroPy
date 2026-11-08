import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from information.audit import audit, demo_data
from information.cli import main


class AuditTests(unittest.TestCase):
    def test_demo_has_known_signal_and_drift(self):
        data, reference = demo_data()
        result = audit(data, "fault", reference)
        values = {row["feature"]: row["mutual_information_bits"] for row in result["features"]}
        self.assertEqual(values["thermal_state"], 1)
        self.assertAlmostEqual(values["alarm"], 0.2780719051126377)
        self.assertEqual(values["zone"], 0)
        self.assertEqual(values["batch"], 0)
        drift = {row["column"]: row["kl_bits"] for row in result["drift"]}
        self.assertAlmostEqual(drift["fault"], 0.20751874963942185)

    def test_infinite_drift_is_valid_json(self):
        result = audit(pd.DataFrame({"x": [0, 1]}), "x", pd.DataFrame({"x": [2, 3]}))
        self.assertIsNone(result["drift"][0]["kl_bits"])
        self.assertEqual(result["drift"][0]["status"], "unseen_in_reference")
        json.dumps(result, allow_nan=False)

    def test_missing_target_and_reference_columns(self):
        data, _ = demo_data()
        with self.assertRaises(ValueError):
            audit(data, "missing")
        with self.assertRaises(ValueError):
            audit(data, "fault", data[["fault"]])

    def test_constant_target_and_cardinality_notes(self):
        result = audit(pd.DataFrame({"constant": [1]*30, "id": range(30)}), "constant")
        self.assertEqual(result["features"][0]["fraction_of_target_information"], 0)
        self.assertTrue(any("constant" in note for note in result["notes"]))
        self.assertTrue(any("distinct states" in note for note in result["notes"]))

    def test_cli_demo_and_csv_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            output = Path(directory)
            self.assertEqual(main(["demo", "--output", str(output)]), 0)
            report = json.loads((output / "audit.json").read_text())
            self.assertEqual(report["rows"], 160)
            self.assertTrue((output / "signal-audit.svg").read_text().startswith("<?xml"))
            self.assertGreater((output / "signal-audit.png").stat().st_size, 1000)
            self.assertEqual(main(["analyze", str(output / "current.csv"), "--target", "fault",
                                   "--reference", str(output / "reference.csv"), "--output", str(output / "again")]), 0)
            repeated = json.loads((output / "again/audit.json").read_text())
            self.assertEqual(report, repeated)

    def test_cli_invalid_file_has_actionable_error(self):
        with contextlib.redirect_stderr(io.StringIO()) as errors, self.assertRaises(SystemExit) as caught:
            main(["analyze", "nonexistent-entropy-input.csv", "--target", "x"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("error:", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
