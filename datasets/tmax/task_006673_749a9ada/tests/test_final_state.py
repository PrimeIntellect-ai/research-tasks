# test_final_state.py
import os
import json
import pytest

def test_results_file_exists():
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"Expected output file {results_path} does not exist."

def test_results_format_and_content():
    results_path = '/home/user/results.json'

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert isinstance(data, list), "The JSON root must be an array (list)."

    # Check structure and keys
    for item in data:
        assert isinstance(item, dict), "Each item in the JSON array must be an object (dictionary)."
        assert set(item.keys()) == {"participant_id", "avg_heart_rate"}, "Each object must have exactly 'participant_id' and 'avg_heart_rate' keys."
        assert isinstance(item["participant_id"], str), "'participant_id' must be a string."
        assert isinstance(item["avg_heart_rate"], (int, float)), "'avg_heart_rate' must be a number."

    # Check sorting
    participant_ids = [item["participant_id"] for item in data]
    assert participant_ids == sorted(participant_ids), "The array must be sorted alphabetically by 'participant_id'."

    # Check expected values
    expected_data = {
        "P001": 72.5,
        "P004": 70.0
    }

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} participant records, found {len(data)}."

    for item in data:
        pid = item["participant_id"]
        assert pid in expected_data, f"Unexpected participant_id '{pid}' in results."

        expected_hr = expected_data[pid]
        actual_hr = item["avg_heart_rate"]

        # Check if it's rounded to 2 decimal places (or equivalent float representation)
        assert round(actual_hr, 2) == actual_hr, f"avg_heart_rate for {pid} is not rounded to 2 decimal places."
        assert abs(actual_hr - expected_hr) < 0.001, f"Expected avg_heart_rate for {pid} to be {expected_hr}, got {actual_hr}."