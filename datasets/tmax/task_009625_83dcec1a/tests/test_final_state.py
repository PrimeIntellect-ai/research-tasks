# test_final_state.py
import os
import json
import pytest

def test_results_file_exists():
    """Test that the results.json file was created."""
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"The results file is missing at {results_path}"
    assert os.path.isfile(results_path), f"The path {results_path} is not a file"

def test_results_content():
    """Test that the results.json file contains the correct selected features and MSE."""
    results_path = "/home/user/results.json"

    with open(results_path, "r", encoding="utf-8") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} does not contain valid JSON.")

    assert "selected_features" in results, "The key 'selected_features' is missing from results.json"
    assert "test_mse" in results, "The key 'test_mse' is missing from results.json"

    expected_features = ["f1", "f2", "f3"]
    actual_features = results["selected_features"]
    assert actual_features == expected_features, (
        f"Expected selected_features to be {expected_features}, "
        f"but got {actual_features}. Check correlation calculation and data leakage."
    )

    expected_mse = 1.0423
    actual_mse = results["test_mse"]
    assert isinstance(actual_mse, (int, float)), f"Expected test_mse to be a number, but got {type(actual_mse).__name__}"
    assert actual_mse == expected_mse, (
        f"Expected test_mse to be {expected_mse}, but got {actual_mse}. "
        "Ensure data leakage is avoided, features are scaled correctly, and MSE is rounded to 4 decimal places."
    )