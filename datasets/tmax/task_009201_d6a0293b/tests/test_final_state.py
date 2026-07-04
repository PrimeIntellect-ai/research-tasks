# test_final_state.py

import os
import json

def test_violations_file_exists():
    file_path = "/home/user/violations.json"
    assert os.path.isfile(file_path), f"File not found: {file_path}. The script did not generate the expected output file."

def test_violations_content():
    file_path = "/home/user/violations.json"
    assert os.path.isfile(file_path), "File not found."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    expected_data = {
        "violations": [
            {
                "user": "U2",
                "reachable_pii_dbs": ["DB1"]
            },
            {
                "user": "U3",
                "reachable_pii_dbs": ["DB1", "DB3"]
            }
        ]
    }

    assert data == expected_data, f"The content of {file_path} does not match the expected violations. Got: {data}"

def test_violations_formatting():
    file_path = "/home/user/violations.json"
    assert os.path.isfile(file_path), "File not found."

    with open(file_path, "r") as f:
        raw_content = f.read()

    # To check 2-space indentation and sorted keys/arrays as per constraints
    with open(file_path, "r") as f:
        data = json.load(f)

    # Dump with 2-space indent
    expected_raw = json.dumps(data, indent=2)

    # We allow minor differences like trailing newlines, but the core structure should match the 2-space indent.
    assert raw_content.strip() == expected_raw.strip(), "The output JSON is not formatted with exactly 2 spaces of indentation or has unexpected formatting."