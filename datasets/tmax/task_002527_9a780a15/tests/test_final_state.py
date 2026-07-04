# test_final_state.py

import os
import json
import pytest

def test_report_json_exists():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"Missing report file: {path}"

def test_report_json_content():
    path = "/home/user/report.json"
    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file")

    required_keys = ["max_abs_error", "cleaned_data_mean", "inference_time_sec"]
    for key in required_keys:
        assert key in report, f"Missing key '{key}' in report.json"
        assert isinstance(report[key], (int, float)), f"Key '{key}' must be a numeric value"

    # The random seed in the setup is fixed, so the expected values are deterministic
    expected_mean = 0.501538
    expected_max_err = 5.96046e-08

    mean_diff = abs(report["cleaned_data_mean"] - expected_mean)
    assert mean_diff < 1e-4, f"Expected cleaned_data_mean ~{expected_mean}, got {report['cleaned_data_mean']}"

    err_diff = abs(report["max_abs_error"] - expected_max_err)
    assert err_diff < 1e-6, f"Expected max_abs_error ~{expected_max_err}, got {report['max_abs_error']}"

    assert report["inference_time_sec"] > 0, "inference_time_sec must be greater than 0"