# test_final_state.py

import os
import json
import pytest

def test_cpp_source_exists():
    file_path = "/home/user/coauthor_query.cpp"
    assert os.path.isfile(file_path), f"C++ source file {file_path} does not exist."

def test_executable_exists():
    file_path = "/home/user/coauthor_query"
    assert os.path.isfile(file_path), f"Executable {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_json_output():
    file_path = "/home/user/coauthors.json"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {file_path} as JSON: {e}")

    expected = [
        {"name": "Dr. Alonzo Church"},
        {"name": "Dr. Claude Shannon"},
        {"name": "Dr. John von Neumann"}
    ]

    assert data == expected, f"JSON output mismatch. Expected {expected}, got {data}"