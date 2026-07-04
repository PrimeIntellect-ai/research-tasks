# test_final_state.py

import os
import json
import pytest

def test_c_source_file_exists():
    file_path = "/home/user/csv_to_json.c"
    assert os.path.exists(file_path), f"C source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_c_executable_exists():
    file_path = "/home/user/csv_to_json"
    assert os.path.exists(file_path), f"Compiled executable {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_page_json_content():
    file_path = "/home/user/page.json"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {file_path} as JSON: {e}")

    expected_data = [
        {"query": {"id": "Q_107"}, "performance": {"time_ms": 670, "scanned": 32000}, "table": "inventory"},
        {"query": {"id": "Q_101"}, "performance": {"time_ms": 450, "scanned": 15000}, "table": "users"},
        {"query": {"id": "Q_110"}, "performance": {"time_ms": 410, "scanned": 18000}, "table": "events"},
        {"query": {"id": "Q_104"}, "performance": {"time_ms": 330, "scanned": 8000}, "table": "products"}
    ]

    assert data == expected_data, f"JSON content in {file_path} does not match the expected paginated results."