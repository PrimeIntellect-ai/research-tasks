# test_final_state.py

import os
import json
import pytest

def test_analysis_report_exists():
    """
    Test that the analysis report JSON file was created.
    """
    file_path = "/home/user/analysis_report.json"
    assert os.path.exists(file_path), f"The analysis report is missing: {file_path}"
    assert os.path.isfile(file_path), f"The path exists but is not a file: {file_path}"

def test_analysis_report_content():
    """
    Test that the analysis report contains the required keys and the values are within the expected ranges.
    """
    file_path = "/home/user/analysis_report.json"

    try:
        with open(file_path, 'r') as f:
            res = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {file_path} does not contain valid JSON.")

    required_keys = ["T_peak", "optimized_mu", "optimized_a", "posterior_mean_c"]
    for key in required_keys:
        assert key in res, f"The JSON file is missing the required key: '{key}'"
        assert isinstance(res[key], (int, float)), f"The value for '{key}' must be a number."

    assert 44.8 <= res["T_peak"] <= 45.2, f"T_peak is out of bounds: {res['T_peak']}"
    assert 44.9 <= res["optimized_mu"] <= 45.1, f"optimized_mu is out of bounds: {res['optimized_mu']}"
    assert 14.5 <= res["optimized_a"] <= 15.5, f"optimized_a is out of bounds: {res['optimized_a']}"
    assert 0.45 <= res["posterior_mean_c"] <= 0.55, f"posterior_mean_c is out of bounds: {res['posterior_mean_c']}"