# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = "/home/user/workspace/valid_webhooks.jsonl"
INPUT_FILE = "/home/user/data/webhooks.jsonl"

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not created."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a regular file."

def test_output_file_content():
    assert os.path.exists(INPUT_FILE), f"Input file {INPUT_FILE} is missing."
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."

    with open(INPUT_FILE, 'r') as f:
        input_lines = f.readlines()

    with open(OUTPUT_FILE, 'r') as f:
        output_lines = f.readlines()

    expected_ids = [i for i in range(1, 1001) if i % 3 != 0 and i % 7 != 0]

    actual_ids = []
    for i, line in enumerate(output_lines):
        try:
            record = json.loads(line)
            actual_ids.append(record.get("id"))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {OUTPUT_FILE} is not valid JSON.")

    assert actual_ids == expected_ids, (
        "The IDs in the output file do not match the expected valid IDs in the correct order. "
        "Ensure you are maintaining the original order and correctly validating the checksums."
    )

    # Check that the exact lines are preserved
    input_dict = {}
    for line in input_lines:
        try:
            record = json.loads(line)
            input_dict[record["id"]] = line
        except json.JSONDecodeError:
            pass

    for i, line in enumerate(output_lines):
        record = json.loads(line)
        expected_line = input_dict[record["id"]]
        assert line == expected_line, (
            f"The output line for id {record['id']} does not exactly match the original input line. "
            "Ensure you write the exact original JSON string with its trailing newline."
        )