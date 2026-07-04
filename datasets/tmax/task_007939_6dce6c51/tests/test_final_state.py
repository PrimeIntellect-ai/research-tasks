# test_final_state.py

import os
import json
import pytest

def test_daily_summary_exists_and_correct():
    summary_path = "/home/user/daily_summary.json"

    assert os.path.exists(summary_path), f"The output file {summary_path} does not exist."
    assert os.path.isfile(summary_path), f"The path {summary_path} is not a file."

    with open(summary_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {summary_path} is not valid JSON.")

    expected = {
        "2023-01-15": 155.0,
        "2023-01-16": 70.0,
        "2023-01-17": 187.5
    }

    assert isinstance(result, dict), f"Expected the JSON root to be a dictionary, got {type(result).__name__}."

    # Check that keys match
    assert set(result.keys()) == set(expected.keys()), f"Expected dates {set(expected.keys())}, got {set(result.keys())}."

    # Check that values match exactly (rounded to 2 decimal places as per instructions)
    for date_key, expected_val in expected.items():
        actual_val = result[date_key]
        assert isinstance(actual_val, float), f"Expected value for {date_key} to be a float, got {type(actual_val).__name__}."
        assert round(actual_val, 2) == expected_val, f"Expected {expected_val} for {date_key}, got {actual_val}."