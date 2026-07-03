# test_final_state.py

import os
import json
import pytest

def test_analyze_go_exists():
    """Test that the Go program analyze.go exists."""
    go_file = "/home/user/analyze.go"
    assert os.path.isfile(go_file), f"File {go_file} does not exist. You must write your Go program here."

def test_results_json_exists():
    """Test that the results.json file was created."""
    results_file = "/home/user/results.json"
    assert os.path.isfile(results_file), f"File {results_file} does not exist. The Go program must generate this file."

def test_results_json_content():
    """Test that the results.json file contains the correct expected values."""
    results_file = "/home/user/results.json"

    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{results_file} is not a valid JSON file.")
    except Exception as e:
        pytest.fail(f"Failed to read {results_file}: {e}")

    # Verify keys exist
    expected_keys = {"clean_row_count", "correlation_f1_f2", "max_eigenvalue"}
    actual_keys = set(data.keys())
    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"results.json is missing expected keys: {missing_keys}"

    # Verify values
    clean_row_count = data.get("clean_row_count")
    assert isinstance(clean_row_count, int), f"clean_row_count must be an integer, got {type(clean_row_count)}"
    assert clean_row_count == 8, f"Expected 8 clean rows, got {clean_row_count}"

    correlation = data.get("correlation_f1_f2")
    assert isinstance(correlation, (int, float)), f"correlation_f1_f2 must be a number, got {type(correlation)}"
    assert round(correlation, 4) == 0.9944, f"Expected correlation_f1_f2 to be approx 0.9944, got {correlation}"

    max_eigenvalue = data.get("max_eigenvalue")
    assert isinstance(max_eigenvalue, (int, float)), f"max_eigenvalue must be a number, got {type(max_eigenvalue)}"
    assert round(max_eigenvalue, 4) == 0.5369, f"Expected max_eigenvalue to be approx 0.5369, got {max_eigenvalue}"