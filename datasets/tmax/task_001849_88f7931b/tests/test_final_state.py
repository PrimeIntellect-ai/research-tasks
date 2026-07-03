# test_final_state.py
import os
import json
import pytest

def test_makefile_exists():
    makefile_path = "/home/user/Makefile"
    assert os.path.exists(makefile_path), f"Makefile is missing at {makefile_path}."
    assert os.path.isfile(makefile_path), f"{makefile_path} is not a file."

def test_schema_gen_executable_exists():
    executable_path = "/home/user/schema_gen"
    assert os.path.exists(executable_path), f"Executable {executable_path} is missing."
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_legacy_b64_exists():
    b64_path = "/home/user/legacy.b64"
    assert os.path.exists(b64_path), f"Base64 output file {b64_path} is missing."
    assert os.path.isfile(b64_path), f"{b64_path} is not a file."

def test_migrated_schema_json():
    json_path = "/home/user/migrated_schema.json"
    assert os.path.exists(json_path), f"Migrated JSON file {json_path} is missing."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_data = [
        {"id": 101, "username": "alice", "joined_date": "2021-01-01", "active": True},
        {"id": 102, "username": "bob", "joined_date": "2022-02-02", "active": True}
    ]

    assert data == expected_data, f"The contents of {json_path} do not match the expected migrated schema."