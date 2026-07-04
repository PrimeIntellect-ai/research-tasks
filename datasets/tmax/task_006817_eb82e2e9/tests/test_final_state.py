# test_final_state.py
import os
import json
import pytest

def test_executables_exist():
    """Test that the compiled executables exist."""
    assert os.path.isfile("/home/user/sim_o2"), "/home/user/sim_o2 executable is missing."
    assert os.access("/home/user/sim_o2", os.X_OK), "/home/user/sim_o2 is not executable."

    assert os.path.isfile("/home/user/sim_o3"), "/home/user/sim_o3 executable is missing."
    assert os.access("/home/user/sim_o3", os.X_OK), "/home/user/sim_o3 is not executable."

def test_profile_report_exists():
    """Test that the profile report JSON exists."""
    assert os.path.isfile("/home/user/profile_report.json"), "/home/user/profile_report.json is missing."

def test_profile_report_content():
    """Test that the profile report JSON contains the correct structure and valid values."""
    report_path = "/home/user/profile_report.json"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "regression_passed" in data, "Missing 'regression_passed' in report."
    assert "mean_diff" in data, "Missing 'mean_diff' in report."
    assert "ci_lower" in data, "Missing 'ci_lower' in report."
    assert "ci_upper" in data, "Missing 'ci_upper' in report."

    assert data["regression_passed"] is True, "'regression_passed' must be true."

    assert isinstance(data["mean_diff"], (float, int)), "'mean_diff' must be a number."
    assert isinstance(data["ci_lower"], (float, int)), "'ci_lower' must be a number."
    assert isinstance(data["ci_upper"], (float, int)), "'ci_upper' must be a number."

    assert data["ci_lower"] < data["ci_upper"], "'ci_lower' must be strictly less than 'ci_upper'."