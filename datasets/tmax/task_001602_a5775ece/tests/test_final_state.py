# test_final_state.py
import os
import json
import pytest

def test_results_json():
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"{results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not a valid JSON file.")

    expected_keys = ['mean_time_ridge', 'mean_time_tree', 't_statistic', 'p_value']
    for k in expected_keys:
        assert k in res, f"Key '{k}' is missing from {results_path}."
        assert isinstance(res[k], (float, int)), f"Value for '{k}' is not a numeric type."

def test_benchmark_plot():
    plot_path = '/home/user/benchmark_plot.png'
    assert os.path.isfile(plot_path), f"{plot_path} does not exist."

    size = os.path.getsize(plot_path)
    assert size > 1000, f"{plot_path} is too small ({size} bytes), likely empty or invalid."

def test_benchmark_script_exists():
    script_path = '/home/user/benchmark.py'
    assert os.path.isfile(script_path), f"{script_path} does not exist."