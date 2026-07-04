# test_final_state.py

import os
import json
import pytest

def test_minimal_crash_log():
    log_path = "/home/user/minimal_crash.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_line = 'ts=2023-10-01T12:00:00Z ip=192.168.1.1 ua="Mozilla/5.0 \\"CrashMe\\"'
    assert content == expected_line, f"minimal_crash.log does not contain the exact expected crash line. Got: {content}"

def test_output_json_exists_and_valid():
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {output_path}, got {type(data).__name__}."
    assert len(data) == 10000, f"Expected exactly 10,000 parsed records in {output_path}, got {len(data)}."

    # Check that the crashing line was parsed
    # The crashing line has user agent: Mozilla/5.0 "CrashMe"
    # We just ensure no empty user agents if the processor logic is right
    for idx, record in enumerate(data):
        assert "user_agent" in record, f"Record at index {idx} is missing 'user_agent' field."
        assert record["user_agent"] != "", f"Record at index {idx} has an empty user agent, which should have failed validation."

def test_processor_assertion_added():
    processor_path = "/home/user/ingester/processor/processor.go"
    assert os.path.isfile(processor_path), f"File {processor_path} is missing."

    with open(processor_path, "r") as f:
        content = f.read()

    expected_error = '"validation failed: empty user agent"'
    assert expected_error in content, f"The required validation error message {expected_error} was not found in {processor_path}."