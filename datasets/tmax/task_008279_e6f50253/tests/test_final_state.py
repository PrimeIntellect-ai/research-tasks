# test_final_state.py

import json
import os
import math

def test_report_exists():
    """Verify that the student generated the report.json file."""
    assert os.path.isfile('/home/user/mlops/report.json'), "The file /home/user/mlops/report.json is missing."

def test_report_contents():
    """Verify the contents of report.json match the expected truth data."""
    report_path = '/home/user/mlops/report.json'
    truth_path = '/home/user/mlops/truth_report.json'

    assert os.path.isfile(truth_path), "Truth report is missing (setup issue)."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "report.json is not a valid JSON file."

    with open(truth_path, 'r') as f:
        truth = json.load(f)

    # Check for presence of required keys
    assert "best_max_depth" in report, "Missing 'best_max_depth' in report.json."
    assert "recommended_run_id" in report, "Missing 'recommended_run_id' in report.json."
    assert "predicted_accuracy" in report, "Missing 'predicted_accuracy' in report.json."

    # Assert values match the expected truth
    assert report["best_max_depth"] == truth["best_max_depth"], \
        f"Incorrect best_max_depth. Expected {truth['best_max_depth']}, got {report['best_max_depth']}."

    assert report["recommended_run_id"] == truth["recommended_run_id"], \
        f"Incorrect recommended_run_id. Expected '{truth['recommended_run_id']}', got '{report['recommended_run_id']}'."

    assert math.isclose(report["predicted_accuracy"], truth["predicted_accuracy"], rel_tol=1e-5), \
        f"Incorrect predicted_accuracy. Expected {truth['predicted_accuracy']}, got {report['predicted_accuracy']}."