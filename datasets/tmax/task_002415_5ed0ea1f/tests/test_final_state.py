# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists_and_valid():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    expected_keys = {"ols_weights", "artifact_weights", "ols_mse", "artifact_mse", "reproducible"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected schema. Found: {list(data.keys())}"

    # Expected values based on the fixed random seed setup
    expected_ols_weights = [1.4883, -1.9962, 0.4996]
    expected_artifact_weights = [1.6, -2.05, 0.7]
    expected_ols_mse = 0.0083
    expected_artifact_mse = 0.0573
    expected_reproducible = False

    # Check ols_weights
    assert len(data["ols_weights"]) == 3, "ols_weights must have exactly 3 elements"
    for i, (val, exp) in enumerate(zip(data["ols_weights"], expected_ols_weights)):
        assert abs(val - exp) <= 0.0002, f"ols_weights[{i}] is {val}, expected {exp}"

    # Check artifact_weights
    assert len(data["artifact_weights"]) == 3, "artifact_weights must have exactly 3 elements"
    for i, (val, exp) in enumerate(zip(data["artifact_weights"], expected_artifact_weights)):
        assert abs(val - exp) <= 0.0002, f"artifact_weights[{i}] is {val}, expected {exp}"

    # Check MSEs
    assert abs(data["ols_mse"] - expected_ols_mse) <= 0.0002, f"ols_mse is {data['ols_mse']}, expected {expected_ols_mse}"
    assert abs(data["artifact_mse"] - expected_artifact_mse) <= 0.0002, f"artifact_mse is {data['artifact_mse']}, expected {expected_artifact_mse}"

    # Check reproducible boolean
    assert data["reproducible"] is expected_reproducible, f"reproducible is {data['reproducible']}, expected {expected_reproducible}"