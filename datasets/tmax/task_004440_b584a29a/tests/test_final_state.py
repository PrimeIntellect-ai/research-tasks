# test_final_state.py

import os
import json
import pytest

def test_report_exists():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"The output file {path} was not created."

def test_report_content():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"The output file {path} was not created."

    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {path} does not contain valid JSON.")

    expected_keys = {"most_drifted_server", "owner_email", "min_rolling_score"}
    missing_keys = expected_keys - set(report.keys())
    assert not missing_keys, f"The report JSON is missing required keys: {missing_keys}"

    assert report["most_drifted_server"] == "srv1", \
        f"Expected most_drifted_server to be 'srv1', got '{report['most_drifted_server']}'"

    assert report["owner_email"] == "alice@example.com", \
        f"Expected owner_email to be 'alice@example.com', got '{report['owner_email']}'"

    expected_score = 0.6389
    actual_score = report["min_rolling_score"]

    assert isinstance(actual_score, (int, float)), \
        f"Expected min_rolling_score to be a number, got {type(actual_score)}"

    assert abs(actual_score - expected_score) < 1e-4, \
        f"Expected min_rolling_score to be approximately {expected_score}, got {actual_score}"