import os
import json
import pytest

def test_experiment_results_exists():
    path = "/home/user/experiment_results.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create the experiment tracking file?"

def test_experiment_results_content():
    path = "/home/user/experiment_results.json"
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "leaky_mse" in data, "Key 'leaky_mse' is missing from experiment_results.json"
    assert "strict_mse" in data, "Key 'strict_mse' is missing from experiment_results.json"

    leaky_mse = data["leaky_mse"]
    strict_mse = data["strict_mse"]

    assert isinstance(leaky_mse, float), "Value for 'leaky_mse' must be a float."
    assert isinstance(strict_mse, float), "Value for 'strict_mse' must be a float."

    expected_leaky = 0.323568
    expected_strict = 0.385718
    epsilon = 1e-4

    assert abs(leaky_mse - expected_leaky) < epsilon, f"Expected leaky_mse to be near {expected_leaky}, but got {leaky_mse}"
    assert abs(strict_mse - expected_strict) < epsilon, f"Expected strict_mse to be near {expected_strict}, but got {strict_mse}"

def test_main_go_exists_and_modified():
    path = "/home/user/ml_pipeline/main.go"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # We expect the file to have been modified to fix the data leakage.
    # While we can't strictly enforce the exact code structure, we can check that it still compiles and runs
    # However, since we are only testing the final state, checking the JSON output is the primary validation.
    # We can at least check it imports gonum.
    assert "gonum.org/v1/gonum/mat" in content, "The modified main.go is missing the gonum matrix library import."