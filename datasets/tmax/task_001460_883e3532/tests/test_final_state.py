# test_final_state.py

import os
import json
import pytest

def test_processed_data_exists():
    file_path = '/home/user/processed_data.jsonl'
    assert os.path.isfile(file_path), f"Output file {file_path} was not created."

def test_processed_data_contents():
    file_path = '/home/user/processed_data.jsonl'

    expected_records = [
        {"ts": "2023-10-01T07:00:00", "id": "S1", "temp": 28.0, "meta": "Early bird"},
        {"ts": "2023-10-01T09:00:00", "id": "S1", "temp": 21.0, "meta": "Restarted with error €"},
        {"ts": "2023-10-01T08:00:00", "id": "S2", "temp": 24.1, "meta": "Initial startup"},
        {"ts": "2023-10-01T09:15:00", "id": "S2", "temp": 20.5, "meta": "Back online all good"}
    ]

    actual_records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {line_num} in {file_path} is not valid JSON: {e}")

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records, but found {len(actual_records)} in {file_path}."
    )

    # Sort both expected and actual to allow for different group orderings
    # but ensure within-group chronological sorting was done correctly.
    def sort_key(r):
        return (r.get("id", ""), r.get("ts", ""))

    expected_sorted = sorted(expected_records, key=sort_key)
    actual_sorted = sorted(actual_records, key=sort_key)

    for i, (exp, act) in enumerate(zip(expected_sorted, actual_sorted)):
        assert act == exp, f"Record mismatch at sorted index {i}. Expected: {exp}, Actual: {act}"

def test_script_exists():
    file_path = '/home/user/etl_pipeline.py'
    assert os.path.isfile(file_path), f"Script {file_path} is missing."