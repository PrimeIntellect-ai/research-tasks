# test_final_state.py

import os
import json
import pytest

def test_regression_report_exists():
    """Check if the regression report JSON file exists."""
    report_path = "/home/user/regression_report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."

def test_regression_report_content():
    """Validate the contents of the regression report JSON file."""
    report_path = "/home/user/regression_report.json"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} is not valid JSON.")

    expected_keys = {"root", "c_forward", "c_backward", "python_true", "more_accurate_method"}
    assert set(data.keys()) == expected_keys, f"The JSON file must contain exactly the keys: {expected_keys}"

    # Check root
    root = data["root"]
    assert isinstance(root, float), "'root' must be a float."
    assert abs(root - 0.25410168836) < 1e-5, f"'root' value {root} is incorrect."

    # Check c_forward and c_backward
    assert isinstance(data["c_forward"], float), "'c_forward' must be a float."
    assert isinstance(data["c_backward"], float), "'c_backward' must be a float."

    # Check python_true
    python_true = data["python_true"]
    assert isinstance(python_true, float), "'python_true' must be a float."
    assert abs(python_true - 0.417983675) < 1e-5, f"'python_true' value {python_true} is incorrect."

    # Check more_accurate_method
    method = data["more_accurate_method"]
    assert method == "backward", f"'more_accurate_method' should be 'backward', but got '{method}'."