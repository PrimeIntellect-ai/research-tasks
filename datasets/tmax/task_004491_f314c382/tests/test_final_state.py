# test_final_state.py
import os
import json
import math

def test_analysis_report_exists():
    file_path = "/home/user/analysis_report.json"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_analysis_report_content():
    file_path = "/home/user/analysis_report.json"
    with open(file_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{file_path} is not a valid JSON file."

    assert "dropped_features" in report, "Missing 'dropped_features' in the report."
    assert "mse" in report, "Missing 'mse' in the report."
    assert "model_weights" in report, "Missing 'model_weights' in the report."

    expected_dropped = ["f2", "f5"]
    actual_dropped = sorted(report["dropped_features"])
    assert actual_dropped == expected_dropped, f"Expected dropped features {expected_dropped}, got {actual_dropped}"

    expected_mse = 0.2081
    actual_mse = report["mse"]
    assert isinstance(actual_mse, (int, float)), "'mse' must be a number."
    assert math.isclose(actual_mse, expected_mse, abs_tol=0.0005), f"MSE mismatch. Expected ~{expected_mse}, got {actual_mse}"

    expected_weights = {
        "f1": 1.8845,
        "f3": 1.4870,
        "f4": -0.4996
    }
    actual_weights = report["model_weights"]
    assert isinstance(actual_weights, dict), "'model_weights' must be a dictionary."

    for k, v in expected_weights.items():
        assert k in actual_weights, f"Missing weight for feature '{k}'."
        assert isinstance(actual_weights[k], (int, float)), f"Weight for '{k}' must be a number."
        assert math.isclose(actual_weights[k], v, abs_tol=0.0005), f"Weight mismatch for '{k}'. Expected ~{v}, got {actual_weights[k]}"

    # Check that no extra weights are present
    extra_weights = set(actual_weights.keys()) - set(expected_weights.keys())
    assert not extra_weights, f"Unexpected weights in 'model_weights': {extra_weights}"