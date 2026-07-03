# test_final_state.py

import os
import json

def test_go_script_exists():
    script_path = "/home/user/parser.go"
    assert os.path.isfile(script_path), f"Go script {script_path} does not exist."

def test_normalized_alerts_jsonl():
    output_path = "/home/user/normalized_alerts.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_data = [
        {"time": "2023-10-24T14:25:01Z", "level": "ERROR", "user": "USR-099", "msg": "Connection timeout in region us-east."},
        {"time": "2023-10-24T14:26:15Z", "level": "WARN", "user": "USR-442", "msg": "Disk usage high on /dev/sda1"},
        {"time": "2023-10-25T09:00:00Z", "level": "ERROR", "user": "USR-102", "msg": "Database lock acquisition failed."},
        {"time": "2024-01-01T00:00:01Z", "level": "WARN", "user": "USR-007", "msg": "Unexpected payload size: 4096 bytes"}
    ]

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_data), f"Expected {len(expected_data)} lines in {output_path}, but found {len(lines)}."

    for i, (line, expected) in enumerate(zip(lines, expected_data)):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} is not valid JSON: {line}"

        assert parsed == expected, f"Line {i+1} JSON content mismatch.\nExpected: {expected}\nGot: {parsed}"