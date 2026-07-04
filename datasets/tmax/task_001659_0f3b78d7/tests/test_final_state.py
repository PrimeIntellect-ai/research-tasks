# test_final_state.py

import os
import json
import pytest

GO_FILE_PATH = "/home/user/etl_extract.go"
OUTPUT_FILE_PATH = "/home/user/summary.jsonl"

def test_go_file_exists():
    assert os.path.exists(GO_FILE_PATH), f"Go source file {GO_FILE_PATH} is missing."
    assert os.path.isfile(GO_FILE_PATH), f"{GO_FILE_PATH} is not a file."

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE_PATH), f"Output file {OUTPUT_FILE_PATH} is missing."
    assert os.path.isfile(OUTPUT_FILE_PATH), f"{OUTPUT_FILE_PATH} is not a file."

def test_output_file_contents():
    with open(OUTPUT_FILE_PATH, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 2, f"Expected exactly 2 lines in {OUTPUT_FILE_PATH}, found {len(lines)}."

    parsed_records = []
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
            parsed_records.append(record)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

    expected_records = {
        "Books": 20.0,
        "Electronics": 200.0
    }

    actual_records = {}
    for record in parsed_records:
        assert "category" in record, "Missing 'category' key in JSON record."
        assert "total_amount" in record, "Missing 'total_amount' key in JSON record."
        actual_records[record["category"]] = float(record["total_amount"])

    assert len(actual_records) == 2, "Expected exactly 2 distinct categories in the output."

    for category, expected_amount in expected_records.items():
        assert category in actual_records, f"Category '{category}' is missing from the output."
        assert actual_records[category] == expected_amount, f"Expected total_amount for '{category}' to be {expected_amount}, but got {actual_records[category]}."