# test_final_state.py
import os
import json
import math
import pytest

def test_rust_project_directory_exists():
    """Verify that the Rust project directory was initialized."""
    project_dir = "/home/user/performance_analysis"
    assert os.path.isdir(project_dir), f"Expected Rust project directory at {project_dir} does not exist."

def test_analysis_results_file_exists():
    """Verify that the analysis_results.json file was created."""
    results_file = "/home/user/analysis_results.json"
    assert os.path.isfile(results_file), f"Expected output file at {results_file} does not exist."

def test_analysis_results_content():
    """Verify the contents and computed statistics in analysis_results.json."""
    results_file = "/home/user/analysis_results.json"

    with open(results_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_file} does not contain valid JSON.")

    required_keys = ["mean_latency_A", "mean_latency_B", "t_stat", "p_value", "correlation"]
    for key in required_keys:
        assert key in data, f"Missing required key '{key}' in {results_file}."

    # Recomputed expected values based on the dataset
    expected_mean_A = 120.0
    expected_mean_B = 90.0
    expected_t_stat = 6.0
    expected_p_value = 0.0003314
    expected_correlation = 0.9856

    assert math.isclose(data["mean_latency_A"], expected_mean_A, rel_tol=1e-3), \
        f"Expected mean_latency_A to be ~{expected_mean_A}, got {data['mean_latency_A']}"

    assert math.isclose(data["mean_latency_B"], expected_mean_B, rel_tol=1e-3), \
        f"Expected mean_latency_B to be ~{expected_mean_B}, got {data['mean_latency_B']}"

    assert math.isclose(abs(data["t_stat"]), expected_t_stat, rel_tol=1e-2), \
        f"Expected absolute t_stat to be ~{expected_t_stat}, got {data['t_stat']}"

    assert math.isclose(data["p_value"], expected_p_value, rel_tol=1e-1), \
        f"Expected p_value to be ~{expected_p_value}, got {data['p_value']}"

    assert math.isclose(data["correlation"], expected_correlation, rel_tol=1e-2), \
        f"Expected correlation to be ~{expected_correlation}, got {data['correlation']}"