# test_final_state.py
import os
import json
import pytest

def test_results_json_exists_and_format():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"The file {results_path} is missing."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not a valid JSON file.")

    expected_keys = {"ci_lower", "ci_upper", "posterior_mean", "most_similar_user_id"}
    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected keys. Found: {list(results.keys())}"

    assert isinstance(results["ci_lower"], (int, float)), "ci_lower must be a number"
    assert isinstance(results["ci_upper"], (int, float)), "ci_upper must be a number"
    assert isinstance(results["posterior_mean"], (int, float)), "posterior_mean must be a number"
    assert isinstance(results["most_similar_user_id"], int), "most_similar_user_id must be an integer"

def test_results_values_match_truth():
    truth_path = '/tmp/ground_truth.json'
    results_path = '/home/user/results.json'

    if not os.path.exists(truth_path):
        pytest.skip("Ground truth file missing, cannot compare values.")

    with open(truth_path, 'r') as f:
        truth = json.load(f)

    with open(results_path, 'r') as f:
        results = json.load(f)

    assert abs(results["ci_lower"] - truth["ci_lower"]) < 1e-3, f"ci_lower is incorrect. Expected approx {truth['ci_lower']}, got {results['ci_lower']}"
    assert abs(results["ci_upper"] - truth["ci_upper"]) < 1e-3, f"ci_upper is incorrect. Expected approx {truth['ci_upper']}, got {results['ci_upper']}"
    assert abs(results["posterior_mean"] - truth["posterior_mean"]) < 1e-3, f"posterior_mean is incorrect. Expected approx {truth['posterior_mean']}, got {results['posterior_mean']}"
    assert results["most_similar_user_id"] == truth["most_similar_user_id"], f"most_similar_user_id is incorrect. Expected {truth['most_similar_user_id']}, got {results['most_similar_user_id']}"

def test_bootstrap_plot_exists_and_valid():
    plot_path = '/home/user/bootstrap_plot.png'
    assert os.path.exists(plot_path), f"The file {plot_path} is missing. Did you fix and run plot.py?"
    assert os.path.isfile(plot_path), f"{plot_path} is not a file."

    size = os.path.getsize(plot_path)
    assert size > 1000, f"The file {plot_path} is too small ({size} bytes). It might be a blank image or corrupted."