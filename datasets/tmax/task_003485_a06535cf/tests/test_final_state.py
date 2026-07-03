# test_final_state.py

import os
import json

def test_processed_logs_exist_and_correct():
    output_path = "/home/user/processed_logs.jsonl"
    assert os.path.exists(output_path), f"Output file {output_path} was not created."
    assert os.path.isfile(output_path), f"{output_path} should be a file."

    expected_lines = [
        {"level": "INFO", "user_id": "101", "action": "login"},
        {"level": "WARN", "user_id": "102", "action": "upload"},
        {"level": "ERROR", "user_id": "103", "action": "delete"},
        {"level": "INFO", "user_id": "104", "action": "logout"},
    ]

    with open(output_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_path}, but found {len(lines)}."

    for i, (actual_line, expected_json) in enumerate(zip(lines, expected_lines)):
        try:
            actual_json = json.loads(actual_line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in {output_path} is not valid JSON: {actual_line}"

        assert actual_json == expected_json, f"Line {i+1} does not match expected output.\nExpected: {expected_json}\nActual: {actual_json}"