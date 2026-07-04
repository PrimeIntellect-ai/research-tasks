# test_final_state.py

import os
import json
import pytest

def test_extracted_metadata_exists():
    path = "/home/user/dataset_work/extracted/metadata.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The archive was not extracted correctly."

def test_valid_metadata_txt():
    path = "/home/user/dataset_work/extracted/valid_metadata.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 valid lines, but found {len(lines)}."

    for line in lines:
        parts = line.split(",")
        assert len(parts) >= 2, f"Line does not appear to be CSV: {line}"
        assert parts[1] == "VALID", f"Expected Status to be 'VALID', got '{parts[1]}' in line: {line}"

def test_go_parser_exists():
    path = "/home/user/dataset_work/parser.go"
    assert os.path.isfile(path), f"Go program {path} does not exist."

def test_result_json():
    path = "/home/user/dataset_work/result.json"
    assert os.path.isfile(path), f"Result file {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "average_temperature" in data, "JSON does not contain 'average_temperature' key."
    assert data["average_temperature"] == 24.2, f"Expected average_temperature to be 24.2, got {data['average_temperature']}"