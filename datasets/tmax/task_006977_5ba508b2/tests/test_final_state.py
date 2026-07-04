# test_final_state.py

import os
import json
import pytest

def test_backup_json_exists_and_valid():
    file_path = "/home/user/backup.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_data = {
        "services": [
            {
                "id": "srv_auth",
                "dependencies": [
                    "srv_cache",
                    "srv_db"
                ]
            },
            {
                "id": "srv_cache",
                "dependencies": []
            },
            {
                "id": "srv_db",
                "dependencies": []
            },
            {
                "id": "srv_queue",
                "dependencies": [
                    "srv_db"
                ]
            }
        ]
    }

    assert data == expected_data, f"JSON content in {file_path} does not match the expected structure."

def test_c_program_exists():
    file_path = "/home/user/map_backup.c"
    assert os.path.isfile(file_path), f"C source file {file_path} does not exist."

def test_binary_exists():
    file_path = "/home/user/map_backup"
    assert os.path.isfile(file_path), f"Compiled binary {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."