# test_final_state.py

import os
import json
import pytest

RESULT_FILE = "/home/user/result.json"
PIPELINE_FILE = "/home/user/pipeline.py"

def test_pipeline_script_exists():
    """Ensure the user created the pipeline script."""
    assert os.path.isfile(PIPELINE_FILE), f"The script {PIPELINE_FILE} was not found."

def test_result_json_exists():
    """Ensure the result.json file was generated."""
    assert os.path.isfile(RESULT_FILE), f"The output file {RESULT_FILE} was not found."

def test_result_json_content():
    """Verify that the result.json contains the correct aggregated and paginated data."""
    with open(RESULT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_FILE} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected the JSON root to be a list, but got {type(data).__name__}."
    assert len(data) == 2, f"Expected exactly 2 records in the output (pagination limit 2), but got {len(data)}."

    expected_data = [
        {
            "department": "HR",
            "avg_tenure": 15.0
        },
        {
            "department": "Analytics",
            "avg_tenure": 12.0
        }
    ]

    for i, expected_record in enumerate(expected_data):
        assert data[i].get("department") == expected_record["department"], \
            f"Record {i+1} department mismatch. Expected '{expected_record['department']}', got '{data[i].get('department')}'."

        # Allow small floating point differences just in case, though it should be exact
        assert abs(float(data[i].get("avg_tenure", 0)) - expected_record["avg_tenure"]) < 1e-5, \
            f"Record {i+1} avg_tenure mismatch. Expected {expected_record['avg_tenure']}, got {data[i].get('avg_tenure')}."