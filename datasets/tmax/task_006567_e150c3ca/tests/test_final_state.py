# test_final_state.py

import os
import json
import pytest

def test_source_file_exists():
    source_file = "/home/user/query_engine.cpp"
    assert os.path.isfile(source_file), f"Source file {source_file} does not exist."

def test_executable_exists():
    executable = "/home/user/query_engine"
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_result_json():
    result_file = "/home/user/result.json"
    assert os.path.isfile(result_file), f"Output file {result_file} does not exist."

    with open(result_file, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {result_file} does not contain valid JSON.")

    expected_data = [
        {"author_id": 1, "name": "Alice", "domain_citations": 230, "coauthor_degree": 3},
        {"author_id": 2, "name": "Bob", "domain_citations": 110, "coauthor_degree": 2}
    ]

    assert data == expected_data, f"JSON content does not match expected output. Got: {data}"