# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists_and_valid_json():
    """Verify that /home/user/report.json exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing: {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert isinstance(data, dict), "JSON root must be a dictionary."

def test_report_contents():
    """Verify the contents of the report.json match the expected deterministic values."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing: {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    # Check keys
    expected_keys = {"best_n_estimators", "best_max_depth", "cv_accuracy", "avg_inference_time_ms"}
    assert expected_keys.issubset(set(data.keys())), f"Missing keys in report.json. Expected: {expected_keys}"

    # Check best_n_estimators
    assert data["best_n_estimators"] == 100, f"Expected best_n_estimators to be 100, got {data['best_n_estimators']}"

    # Check best_max_depth
    assert data["best_max_depth"] is None, f"Expected best_max_depth to be null (None), got {data['best_max_depth']}"

    # Check cv_accuracy
    assert data["cv_accuracy"] == 0.9381, f"Expected cv_accuracy to be 0.9381, got {data['cv_accuracy']}"

    # Check avg_inference_time_ms
    avg_time = data["avg_inference_time_ms"]
    assert isinstance(avg_time, float), f"Expected avg_inference_time_ms to be a float, got {type(avg_time)}"
    assert avg_time > 0, f"Expected avg_inference_time_ms to be > 0, got {avg_time}"