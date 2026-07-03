# test_final_state.py

import os
import json
import pytest

def test_processed_results_exists():
    """Test that the processed_results.json file exists."""
    file_path = '/home/user/processed_results.json'
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_processed_results_content():
    """Test that the processed_results.json file contains the correct results."""
    file_path = '/home/user/processed_results.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} is not valid JSON.")

    assert "pattern_matches" in data, "The 'pattern_matches' key is missing from the JSON data."
    assert "shortest_path_length" in data, "The 'shortest_path_length' key is missing from the JSON data."

    # Verify pattern matches
    expected_matches = [
        ["Dr. Alice", "Dr. Bob"],
        ["Dr. Alice", "Dr. Diana"],
        ["Dr. Bob", "Dr. Diana"]
    ]
    actual_matches = data["pattern_matches"]

    assert isinstance(actual_matches, list), "'pattern_matches' should be a list."
    assert actual_matches == expected_matches, (
        f"Pattern matches do not match expected output.\n"
        f"Expected: {expected_matches}\n"
        f"Actual: {actual_matches}"
    )

    # Verify shortest path length
    expected_path_length = 4
    actual_path_length = data["shortest_path_length"]

    assert isinstance(actual_path_length, int), "'shortest_path_length' should be an integer."
    assert actual_path_length == expected_path_length, (
        f"Shortest path length does not match expected output.\n"
        f"Expected: {expected_path_length}\n"
        f"Actual: {actual_path_length}"
    )