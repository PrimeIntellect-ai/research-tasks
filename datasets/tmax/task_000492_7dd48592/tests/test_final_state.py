# test_final_state.py
import json
import os
import pytest

def test_result_json_exists():
    result_path = "/home/user/result.json"
    assert os.path.exists(result_path), f"The file {result_path} does not exist."
    assert os.path.isfile(result_path), f"The path {result_path} is not a file."

def test_result_json_format_and_metric():
    result_path = "/home/user/result.json"

    try:
        with open(result_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {result_path} as JSON: {e}")

    assert "CoM" in data, "Key 'CoM' is missing from result.json."
    com = data["CoM"]
    for axis in ["x", "y", "z"]:
        assert axis in com, f"Key '{axis}' is missing from 'CoM' in result.json."
        assert isinstance(com[axis], (int, float)), f"CoM '{axis}' must be a numeric value."

    assert "ConfidenceInterval_95" in data, "Key 'ConfidenceInterval_95' is missing from result.json."
    ci = data["ConfidenceInterval_95"]
    expected_ci_keys = ["x_lower", "x_upper", "y_lower", "y_upper", "z_lower", "z_upper"]
    for key in expected_ci_keys:
        assert key in ci, f"Key '{key}' is missing from 'ConfidenceInterval_95' in result.json."
        assert isinstance(ci[key], (int, float)), f"ConfidenceInterval_95 '{key}' must be a numeric value."

    # The true CoM is derived from the cluster_sim generation logic:
    # 2,500,000 pairs, each pair sums to exactly 1e-4 for x, y, z.
    # Total mass = 5,000,000.
    # True CoM = (2,500,000 * 1e-4) / 5,000,000 = 5e-5
    true_val = 5e-5

    mae = max(
        abs(com["x"] - true_val),
        abs(com["y"] - true_val),
        abs(com["z"] - true_val)
    )

    threshold = 1e-10
    assert mae < threshold, (
        f"Maximum Absolute Error (MAE) threshold not met. "
        f"Measured MAE: {mae}, Threshold: {threshold}. "
        f"Computed CoM: {com}. Expected CoM: {true_val} for all axes."
    )