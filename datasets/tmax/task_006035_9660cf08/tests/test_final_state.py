# test_final_state.py

import os
import json
import pytest

def test_go_source_file_exists():
    file_path = "/home/user/bootstrap_mcmc.go"
    assert os.path.exists(file_path), f"The Go source file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_json_output_file_exists():
    file_path = "/home/user/posterior_summary.json"
    assert os.path.exists(file_path), f"The JSON output file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_json_output_contents():
    file_path = "/home/user/posterior_summary.json"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    assert "mean" in data, "The JSON output is missing the 'mean' key."
    assert "ci_lower" in data, "The JSON output is missing the 'ci_lower' key."
    assert "ci_upper" in data, "The JSON output is missing the 'ci_upper' key."

    mean = data["mean"]
    ci_lower = data["ci_lower"]
    ci_upper = data["ci_upper"]

    assert isinstance(mean, (int, float)), f"Expected 'mean' to be a number, got {type(mean)}"
    assert isinstance(ci_lower, (int, float)), f"Expected 'ci_lower' to be a number, got {type(ci_lower)}"
    assert isinstance(ci_upper, (int, float)), f"Expected 'ci_upper' to be a number, got {type(ci_upper)}"

    assert abs(mean - 2.41) < 1e-4, f"Mean incorrect: expected ~2.41, got {mean}"
    assert 1.8 <= ci_lower <= 2.3, f"ci_lower out of expected range (1.8 - 2.3): got {ci_lower}"
    assert 2.5 <= ci_upper <= 3.1, f"ci_upper out of expected range (2.5 - 3.1): got {ci_upper}"