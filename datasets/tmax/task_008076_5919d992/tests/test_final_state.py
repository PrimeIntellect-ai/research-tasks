# test_final_state.py

import os
import json
import re
import pytest

def test_failed_attempts_file():
    """Verify that the EXTRACT step created failed_attempts.txt with correct lines."""
    file_path = "/home/user/failed_attempts.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did the EXTRACT step run?"

    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected 3 lines in {file_path}, but found {len(lines)}."
    for line in lines:
        assert "Failed password" in line, f"Line missing 'Failed password': {line}"

def test_structured_data_json():
    """Verify that the TRANSFORM step created valid JSON with the correct extracted data."""
    file_path = "/home/user/structured_data.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did the TRANSFORM step run?"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    expected_data = [
        {"timestamp": "Jan 15 10:15:22", "user": "admin", "ip": "192.168.1.50"},
        {"timestamp": "Jan 15 10:17:10", "user": "root", "ip": "10.0.0.5"},
        {"timestamp": "Jan 15 10:20:00", "user": "testuser", "ip": "172.16.0.4"}
    ]

    assert isinstance(data, list), f"Expected a JSON array in {file_path}, but got {type(data).__name__}."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in JSON array, got {len(data)}."

    for i, expected_item in enumerate(expected_data):
        assert data[i] == expected_item, f"Mismatch at index {i} in {file_path}. Expected {expected_item}, got {data[i]}."

def test_pipeline_log():
    """Verify that the pipeline execution was logged correctly."""
    file_path = "/home/user/pipeline.log"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Pipeline logging step failed."

    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, but found {len(lines)}."

    extract_pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] EXTRACT SUCCESS$"
    transform_pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] TRANSFORM SUCCESS$"

    assert re.match(extract_pattern, lines[0]), f"First line of log does not match expected format. Got: {lines[0]}"
    assert re.match(transform_pattern, lines[1]), f"Second line of log does not match expected format. Got: {lines[1]}"