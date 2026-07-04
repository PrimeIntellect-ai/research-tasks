# test_final_state.py

import os
import json

def test_script_exists_and_executable():
    """Test that the clean.sh script exists and is executable."""
    script_path = "/home/user/clean.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_output_file_exists():
    """Test that the clean_data.jsonl file exists."""
    output_path = "/home/user/clean_data.jsonl"
    assert os.path.isfile(output_path), f"{output_path} does not exist."

def test_output_content():
    """Test that the clean_data.jsonl file contains the correctly transformed JSON objects."""
    output_path = "/home/user/clean_data.jsonl"
    assert os.path.isfile(output_path), f"{output_path} does not exist."

    expected_objects = [
        {
            "email": "***@gmail.com",
            "email_domain": "gmail.com",
            "message": "Hello",
            "timestamp": "2023-01-01T00:00:00Z",
            "user_name": "José"
        },
        {
            "email": "***@company.org",
            "email_domain": "company.org",
            "message": "Test",
            "timestamp": "2023-01-02T15:30:00Z",
            "user_name": "Müller"
        },
        {
            "email": "***@localhost.local",
            "email_domain": "localhost.local",
            "message": "System startup",
            "timestamp": "2023-01-03T17:00:00Z",
            "user_name": "テスト"
        },
        {
            "email": "***@sub.domain.co.uk",
            "email_domain": "sub.domain.co.uk",
            "name": "François",
            "notes": "None",
            "timestamp": "2023-10-31T08:15:45Z"
        }
    ]

    actual_objects = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_objects.append(json.loads(line))
            except json.JSONDecodeError:
                assert False, f"Invalid JSON found in {output_path}: {line}"

    assert len(actual_objects) == len(expected_objects), \
        f"Expected {len(expected_objects)} JSON objects, found {len(actual_objects)}."

    for i, (expected, actual) in enumerate(zip(expected_objects, actual_objects)):
        assert actual == expected, f"Object at line {i+1} does not match expected output.\nExpected: {expected}\nActual: {actual}"