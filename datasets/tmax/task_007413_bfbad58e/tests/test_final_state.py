# test_final_state.py

import os
import json
import pytest

def test_trace_summary_exists():
    """Verify that the output JSON file exists."""
    assert os.path.isfile("/home/user/trace_summary.json"), "The file /home/user/trace_summary.json is missing."

def test_trace_summary_contents():
    """Verify that the contents of the output JSON file match the expected trace summary."""
    with open("/home/user/trace_summary.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/trace_summary.json is not valid JSON.")

    expected_data = [
        {"trace_id": "T100", "duration_ms": 3000, "max_db_query_ms": 45, "has_error": False},
        {"trace_id": "T101", "duration_ms": 2000, "max_db_query_ms": 120, "has_error": True},
        {"trace_id": "T102", "duration_ms": 6000, "max_db_query_ms": 200, "has_error": False}
    ]

    assert isinstance(data, list), "The JSON root must be an array."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} traces, but found {len(data)}."

    # Check sorting by trace_id
    trace_ids = [item.get("trace_id") for item in data]
    assert trace_ids == sorted(trace_ids), "The JSON array is not sorted alphabetically by trace_id."

    for i in range(len(expected_data)):
        assert data[i] == expected_data[i], f"Mismatch at index {i}. Expected {expected_data[i]}, got {data[i]}."