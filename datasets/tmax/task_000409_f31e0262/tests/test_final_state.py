# test_final_state.py
import os
import json
import pytest

def test_benchmark_results_exists():
    json_path = "/home/user/benchmark_results.json"
    assert os.path.exists(json_path), f"The file {json_path} does not exist. Did you run your evaluate_etl.py script?"
    assert os.path.isfile(json_path), f"The path {json_path} is not a file."

def test_benchmark_results_content():
    json_path = "/home/user/benchmark_results.json"
    if not os.path.exists(json_path):
        pytest.skip(f"{json_path} is missing.")

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_keys = {"mean_diff", "t_statistic", "p_value", "reject_null"}
    actual_keys = set(results.keys())
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}."

    assert isinstance(results["mean_diff"], float), "The value for 'mean_diff' must be a float."
    assert isinstance(results["t_statistic"], float), "The value for 't_statistic' must be a float."
    assert isinstance(results["p_value"], float), "The value for 'p_value' must be a float."
    assert isinstance(results["reject_null"], bool), "The value for 'reject_null' must be a boolean."

    assert 0.0 <= results["p_value"] <= 1.0, f"The 'p_value' ({results['p_value']}) must be between 0.0 and 1.0."

def test_evaluate_etl_script_exists():
    script_path = "/home/user/evaluate_etl.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing. You need to create it."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."