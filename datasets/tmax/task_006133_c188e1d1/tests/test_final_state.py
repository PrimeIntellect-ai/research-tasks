# test_final_state.py

import os
import json
import sqlite3
import pytest

OUTPUT_JSON_PATH = '/home/user/department_summary.json'
SCRIPT_PATH = '/home/user/etl_pipeline.py'
DB_PATH = '/home/user/legacy_corp.db'

def test_script_exists():
    """Test that the ETL pipeline script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_output_json_exists_and_valid():
    """Test that the output JSON file exists and contains valid JSON."""
    assert os.path.exists(OUTPUT_JSON_PATH), f"Output JSON not found at {OUTPUT_JSON_PATH}"
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Path {OUTPUT_JSON_PATH} is not a file"

    with open(OUTPUT_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} does not contain valid JSON")

    assert isinstance(data, dict), "The JSON output must be a single JSON object (dictionary)"

def test_output_json_content():
    """Test that the output JSON contains the correct aggregated data and keys are sorted."""
    with open(OUTPUT_JSON_PATH, 'r') as f:
        data = json.load(f)

    expected_data = {
        "PRJ-A": 35,
        "PRJ-B": 45,
        "PRJ-C": 5
    }

    assert data == expected_data, f"JSON content does not match expected output. Got: {data}"

    # Check if keys are sorted alphabetically
    keys = list(data.keys())
    assert keys == sorted(keys), "The keys in the JSON object are not sorted alphabetically"