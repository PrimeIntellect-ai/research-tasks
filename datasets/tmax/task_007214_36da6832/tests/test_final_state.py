# test_final_state.py

import os
import json
import pytest

def test_hourly_summary_exists_and_correct():
    summary_path = "/home/user/hourly_summary.json"

    assert os.path.isfile(summary_path), f"Output file {summary_path} is missing."

    with open(summary_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} is not a valid JSON file.")

    expected_data = {
        "2023-10-25T14:00:00Z": {
            "web": 2
        },
        "2023-10-25T15:00:00Z": {
            "db": 1,
            "web": 1
        },
        "2023-10-26T09:00:00Z": {
            "db": 1
        }
    }

    assert data == expected_data, f"Content of {summary_path} does not match expected aggregation."

def test_quarantine_exists_and_correct():
    quarantine_path = "/home/user/quarantine.jsonl"

    assert os.path.isfile(quarantine_path), f"Output file {quarantine_path} is missing."

    with open(quarantine_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    expected_lines = [
        r'{"timestamp": "2023-10-25T14:50:00Z", "service": "api", "action": "update", "details": "corrupted unicode \u12X4 error"}',
        r'{"timestamp": "2023-10-25T15:42:00Z", "service": "api", "action": "restart", "details": "bad escape \uZZZZ crash"}'
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {quarantine_path}, found {len(lines)}."

    for i, expected_line in enumerate(expected_lines):
        assert lines[i] == expected_line, f"Line {i+1} in {quarantine_path} does not match the expected raw string."