# test_final_state.py

import os
import json
import pytest

def test_output_file_exists():
    output_path = "/home/user/output.jsonl"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_output_content_and_format():
    output_path = "/home/user/output.jsonl"
    with open(output_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 4, f"Expected 4 JSON lines in the output, but found {len(lines)}."

    parsed_lines = []
    for i, line in enumerate(lines):
        try:
            parsed_lines.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

    expected_data = [
        {
            "interval": "2023-11-01T08:00:00Z",
            "event_id": "EVT-001",
            "severity": "INFO",
            "message": "Service started successfully"
        },
        {
            "interval": "2023-11-01T08:00:00Z",
            "event_id": "EVT-002",
            "severity": "WARN",
            "message": "Memory usage high\nConsider upgrading instance"
        },
        {
            "interval": "2023-11-01T09:00:00Z",
            "event_id": "EVT-004",
            "severity": "ERROR",
            "message": "Database connection lost\nRetrying in 5 seconds..."
        },
        {
            "interval": "2023-11-01T09:00:00Z",
            "event_id": "EVT-006",
            "severity": "INFO",
            "message": "User logged in"
        }
    ]

    for i, (actual, expected) in enumerate(zip(parsed_lines, expected_data)):
        assert actual == expected, f"Mismatch at line {i+1}.\nExpected: {expected}\nActual: {actual}"