# test_final_state.py

import os
import json
import pytest

def test_anomalies_json_exists():
    """Test that the output file anomalies.json exists."""
    output_path = "/home/user/anomalies.json"
    assert os.path.exists(output_path), f"The file {output_path} was not created."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

def test_anomalies_json_content():
    """Test that anomalies.json contains the correct data."""
    output_path = "/home/user/anomalies.json"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The root of the JSON file should be a list, got {type(data).__name__}."

    expected_data = [
        {"minute": "2023-10-24 10:05", "rolling_avg": 3.67},
        {"minute": "2023-10-24 10:06", "rolling_avg": 4.33},
        {"minute": "2023-10-24 10:07", "rolling_avg": 4.33}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} anomalies, but found {len(data)}."

    for i, expected_item in enumerate(expected_data):
        assert "minute" in data[i], f"Item at index {i} is missing the 'minute' key."
        assert "rolling_avg" in data[i], f"Item at index {i} is missing the 'rolling_avg' key."

        assert data[i]["minute"] == expected_item["minute"], f"Expected minute {expected_item['minute']} at index {i}, got {data[i]['minute']}."

        # Using a small tolerance for floating point comparison
        actual_avg = data[i]["rolling_avg"]
        expected_avg = expected_item["rolling_avg"]
        assert isinstance(actual_avg, (int, float)), f"rolling_avg at index {i} should be a number."
        assert abs(actual_avg - expected_avg) < 0.011, f"Expected rolling_avg {expected_avg} at index {i}, got {actual_avg}."