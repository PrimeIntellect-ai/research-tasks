# test_final_state.py

import os
import json
import csv
import hashlib
import pytest

def get_input_data():
    input_path = "/home/user/input_events.json"
    assert os.path.exists(input_path), f"Input file {input_path} is missing."
    with open(input_path, 'r') as f:
        return json.load(f)

def test_scripts_exist_and_executable():
    """Test that the required scripts exist and run.sh is executable."""
    assert os.path.exists("/home/user/mask.py"), "/home/user/mask.py is missing."
    assert os.path.exists("/home/user/extract.js"), "/home/user/extract.js is missing."

    run_sh_path = "/home/user/run.sh"
    assert os.path.exists(run_sh_path), f"{run_sh_path} is missing."
    assert os.access(run_sh_path, os.X_OK), f"{run_sh_path} is not executable."

def test_masked_csv_output():
    """Test the intermediate output of Stage 1 (mask.py)."""
    csv_path = "/home/user/masked.csv"
    assert os.path.exists(csv_path), f"Intermediate CSV file {csv_path} is missing."

    input_data = get_input_data()
    expected_rows = []
    for row in input_data:
        email_hash = hashlib.sha256(row['email'].encode('utf-8')).hexdigest()
        expected_rows.append({
            'id': str(row['id']),
            'email_hash': email_hash,
            'event_type': row['event_type'],
            'value': str(row['value'])
        })

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None, "CSV file has no header."

        # Check exact header names
        expected_headers = ['id', 'email_hash', 'event_type', 'value']
        assert reader.fieldnames == expected_headers, f"CSV headers {reader.fieldnames} do not match expected {expected_headers}."

        actual_rows = list(reader)
        assert len(actual_rows) == len(expected_rows), "Incorrect number of rows in CSV."

        for actual, expected in zip(actual_rows, expected_rows):
            assert actual == expected, f"CSV row mismatch: expected {expected}, got {actual}."

def test_final_features_jsonl():
    """Test the final output of Stage 2 (extract.js)."""
    jsonl_path = "/home/user/final_features.jsonl"
    assert os.path.exists(jsonl_path), f"Final output file {jsonl_path} is missing."

    input_data = get_input_data()
    expected_lines = []
    for row in input_data:
        email_hash = hashlib.sha256(row['email'].encode('utf-8')).hexdigest()
        value_category = "HIGH" if row['value'] > 50 else "LOW"
        expected_lines.append({
            'id': row['id'],
            'email_hash': email_hash,
            'event_type': row['event_type'],
            'value_category': value_category
        })

    with open(jsonl_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in JSONL, got {len(lines)}."

    for i, (line, expected) in enumerate(zip(lines, expected_lines)):
        try:
            actual = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {jsonl_path} is not valid JSON.")

        assert actual == expected, f"JSON object mismatch on line {i+1}: expected {expected}, got {actual}."