# test_final_state.py
import os
import json
import pytest

def test_output_file_exists():
    output_file = "/home/user/processed/output.jsonl"
    assert os.path.exists(output_file), f"Error: {output_file} does not exist. The ETL pipeline must generate this file."

def test_output_file_content():
    output_file = "/home/user/processed/output.jsonl"
    assert os.path.exists(output_file), f"Error: {output_file} does not exist."

    expected_records = [
        {
            "id": "1", 
            "name": "Alice Smith", 
            "email": "alice@example.com", 
            "dob": "1990-01-01", 
            "ssn": "***-**-6789", 
            "notes": "Regular user"
        },
        {
            "id": "2", 
            "name": "Bob Jones", 
            "email": "bob@example.com", 
            "dob": "1985-05-15", 
            "ssn": "***-**-4321", 
            "notes": "This is a multiline\nnote for Bob.\nIt has newlines."
        },
        {
            "id": "5", 
            "name": "Eve Davis", 
            "email": "eve@example.com", 
            "dob": "1995-12-31", 
            "ssn": "***-**-5555", 
            "notes": "Valid user record"
        }
    ]

    actual_records = []
    try:
        with open(output_file, 'r') as f:
            for line in f:
                if line.strip():
                    actual_records.append(json.loads(line.strip()))
    except Exception as e:
        pytest.fail(f"Error reading JSONL file: {e}. Ensure the file contains valid JSON per line.")

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} valid records, but found {len(actual_records)}. Check your deduplication and validation logic."

    for i, (expected, actual) in enumerate(zip(expected_records, actual_records)):
        assert expected == actual, f"Record at index {i} does not match expected output.\nExpected: {expected}\nActual: {actual}"