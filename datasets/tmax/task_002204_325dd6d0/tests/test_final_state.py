# test_final_state.py
import os
import json
import pytest

def test_process_go_exists():
    path = "/home/user/process.go"
    assert os.path.isfile(path), f"File {path} does not exist. The Go program was not created."
    assert os.path.getsize(path) > 0, f"File {path} is empty."

def test_recommendations_json_exists():
    path = "/home/user/recommendations.json"
    assert os.path.isfile(path), f"File {path} does not exist. The Go program might not have been run or didn't output the file."
    assert os.path.getsize(path) > 0, f"File {path} is empty."

def test_recommendations_match_expected():
    expected_path = "/home/user/expected_recs.json"
    actual_path = "/home/user/recommendations.json"

    assert os.path.isfile(expected_path), f"Expected truth file {expected_path} is missing."
    assert os.path.isfile(actual_path), f"Actual output file {actual_path} is missing."

    with open(expected_path, 'r') as f:
        expected_data = json.load(f)

    with open(actual_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {actual_path} does not contain valid JSON.")

    assert isinstance(actual_data, dict), "The output JSON should be an object (dictionary)."
    assert len(actual_data) == 100, f"Expected 100 keys in the output, got {len(actual_data)}."

    for key, expected_val in expected_data.items():
        assert key in actual_data, f"Key '{key}' is missing from the output."
        actual_val = actual_data[key]
        assert isinstance(actual_val, list), f"Value for key '{key}' should be a list, got {type(actual_val)}."
        assert len(actual_val) == 2, f"Expected 2 recommendations for key '{key}', got {len(actual_val)}."
        assert actual_val == expected_val, f"Recommendations for key '{key}' do not match. Expected {expected_val}, got {actual_val}."