# test_final_state.py

import os
import json
import pytest

def test_output_jsonl_content():
    output_path = "/home/user/dataset/output.jsonl"

    # 1. Verify output file exists
    assert os.path.exists(output_path), f"Output file not found: {output_path}"
    assert os.path.isfile(output_path), f"Output path is not a file: {output_path}"

    expected_data = [
        {"participant_id": "S01", "response_time": "450", "accuracy": "0.95"},
        {"participant_id": "S02", "response_time": "510", "accuracy": "0.88"},
        {"participant_id": "S03", "response_time": "480", "accuracy": "0.92"}
    ]

    # 2. Read the lines and parse them as JSON
    actual_data = []
    with open(output_path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed_line = json.loads(line)
                actual_data.append(parsed_line)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON on line {line_num} in {output_path}: {e}")

    # 3. Check that the extracted dictionaries match the expected output exactly
    assert len(actual_data) == len(expected_data), (
        f"Expected {len(expected_data)} lines in output.jsonl, "
        f"but found {len(actual_data)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, (
            f"Mismatch at line {i + 1} in {output_path}.\n"
            f"Expected: {expected}\n"
            f"Got:      {actual}"
        )