# test_final_state.py

import os
import json
import pytest

def test_parsed_logs_exist_and_correct():
    output_file = "/home/user/ticket_8412/parsed_logs.jsonl"

    assert os.path.exists(output_file), f"The output file {output_file} does not exist. Did you run the script?"
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    parsed_lines = []
    with open(output_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed_data = json.loads(line)
                parsed_lines.append(parsed_data)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {output_file} is not valid JSON: {line}")

    assert len(parsed_lines) == 5, f"Expected 5 parsed log entries, found {len(parsed_lines)}."

    # Verify the edge-case line
    edge_case_found = False
    for entry in parsed_lines:
        assert "time" in entry, "Missing 'time' key in JSON object."
        assert "level" in entry, "Missing 'level' key in JSON object."
        assert "message" in entry, "Missing 'message' key in JSON object."

        if entry["time"] == "2023-10-12 10:05:00":
            edge_case_found = True
            assert entry["level"] == "WARN", f"Expected level 'WARN', got {entry['level']}"
            expected_msg = "[AuthService] Failed login attempt for user [admin]"
            assert entry["message"] == expected_msg, f"Expected message '{expected_msg}', got '{entry['message']}'"

    assert edge_case_found, "The edge-case log entry for 10:05:00 was not found in the output file."

def test_all_logs_parsed_correctly():
    output_file = "/home/user/ticket_8412/parsed_logs.jsonl"
    if not os.path.exists(output_file):
        pytest.skip("Output file missing, skipping detailed checks.")

    expected_logs = [
        {"time": "2023-10-12 10:00:00", "level": "INFO", "message": "Service started successfully"},
        {"time": "2023-10-12 10:01:15", "level": "DEBUG", "message": "Connecting to database at localhost:5432"},
        {"time": "2023-10-12 10:02:30", "level": "ERROR", "message": "Connection lost - retrying in 5s"},
        {"time": "2023-10-12 10:05:00", "level": "WARN", "message": "[AuthService] Failed login attempt for user [admin]"},
        {"time": "2023-10-12 10:06:00", "level": "INFO", "message": "Service stopped"}
    ]

    with open(output_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_logs), "The number of lines in the output file does not match the input logs."

    for i, expected in enumerate(expected_logs):
        actual = json.loads(lines[i])
        assert actual == expected, f"Log entry {i+1} does not match expected output.\nExpected: {expected}\nActual: {actual}"