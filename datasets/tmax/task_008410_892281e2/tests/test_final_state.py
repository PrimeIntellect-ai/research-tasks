# test_final_state.py

import os
import json
import pytest

SUMMARY_PATH = '/home/user/daily_summary.json'

def test_summary_file_exists():
    assert os.path.exists(SUMMARY_PATH), f"Expected output file {SUMMARY_PATH} does not exist."
    assert os.path.isfile(SUMMARY_PATH), f"Path {SUMMARY_PATH} is not a file."

def test_summary_json_validity():
    with open(SUMMARY_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SUMMARY_PATH} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected the JSON root to be a list, got {type(data).__name__}."

def test_summary_contents():
    with open(SUMMARY_PATH, 'r') as f:
        data = json.load(f)

    expected_data = [
        {
            "date": "2023-10-01",
            "max_temperature": 22.5,
            "avg_humidity": 47.5
        },
        {
            "date": "2023-10-02",
            "max_temperature": 19.0,
            "avg_humidity": 60.0
        },
        {
            "date": "2023-10-03",
            "max_temperature": 28.0,
            "avg_humidity": 52.5
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert "date" in actual, f"Record {i} is missing 'date' key."
        assert "max_temperature" in actual, f"Record {i} is missing 'max_temperature' key."
        assert "avg_humidity" in actual, f"Record {i} is missing 'avg_humidity' key."

        assert actual["date"] == expected["date"], f"Expected date {expected['date']} at index {i}, got {actual['date']}."

        # Check max_temperature
        assert isinstance(actual["max_temperature"], (int, float)), f"max_temperature must be a number at index {i}."
        assert abs(actual["max_temperature"] - expected["max_temperature"]) < 1e-5, f"Expected max_temperature {expected['max_temperature']} for date {expected['date']}, got {actual['max_temperature']}."

        # Check avg_humidity
        assert isinstance(actual["avg_humidity"], (int, float)), f"avg_humidity must be a number at index {i}."
        assert abs(actual["avg_humidity"] - expected["avg_humidity"]) < 1e-5, f"Expected avg_humidity {expected['avg_humidity']} for date {expected['date']}, got {actual['avg_humidity']}."

def test_summary_sorted():
    with open(SUMMARY_PATH, 'r') as f:
        data = json.load(f)

    dates = [row.get("date") for row in data if isinstance(row, dict) and "date" in row]
    assert dates == sorted(dates), "The JSON array is not sorted chronologically by date."