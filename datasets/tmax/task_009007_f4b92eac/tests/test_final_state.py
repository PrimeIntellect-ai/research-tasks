# test_final_state.py

import os
import json
import pytest

def test_test_results_file_exists():
    assert os.path.isfile("/home/user/test_results.json"), "/home/user/test_results.json file is missing. The script did not produce the expected output file."

def test_test_results_content():
    file_path = "/home/user/test_results.json"

    with open(file_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    # Check keys
    assert "accuracy" in results, "Missing 'accuracy' key in test_results.json"
    assert "passed" in results, "Missing 'passed' key in test_results.json"
    assert "predictions" in results, "Missing 'predictions' key in test_results.json"

    # Check accuracy
    assert isinstance(results["accuracy"], (int, float)), "'accuracy' must be a number."
    assert results["accuracy"] == 1.0, f"Expected accuracy to be 1.0, but got {results['accuracy']}."

    # Check passed flag
    assert isinstance(results["passed"], bool), "'passed' must be a boolean."
    assert results["passed"] is True, "Expected 'passed' to be true."

    # Check predictions
    predictions = results["predictions"]
    assert isinstance(predictions, list), "'predictions' must be a list."
    assert len(predictions) == 20, f"Expected exactly 20 predictions, but got {len(predictions)}."

    expected_predictions = [
        "Electronics" if i % 2 == 0 else "Clothing"
        for i in range(20)
    ]

    assert predictions == expected_predictions, "The predicted categories do not match the expected pattern."