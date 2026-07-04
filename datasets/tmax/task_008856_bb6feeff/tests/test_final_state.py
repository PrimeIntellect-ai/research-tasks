# test_final_state.py
import os
import json
import pytest

def test_averages_json():
    filepath = "/home/user/output/averages.json"
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did you create the output directory and save the file?"

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} is not valid JSON")

    expected = {
        "Alpha": 26.0,
        "Beta": 105.0,
        "Gamma": 50.0
    }

    assert data == expected, f"Contents of {filepath} do not match expected values. Expected {expected}, got {data}"

def test_pipeline_stats_json():
    filepath = "/home/user/logs/pipeline_stats.json"
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did you create the logs directory and save the file?"

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} is not valid JSON")

    expected = {
        "total_records_read": 10,
        "duplicates_dropped": 3,
        "unique_sensors_found": 3
    }

    assert data == expected, f"Contents of {filepath} do not match expected values. Expected {expected}, got {data}"