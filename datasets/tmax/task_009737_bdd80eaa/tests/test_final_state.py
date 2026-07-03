# test_final_state.py

import os
import json
import pytest

def test_c_source_and_executable_exist():
    """Verify that the C source code and the compiled executable exist."""
    source_path = "/home/user/build_paths.c"
    exec_path = "/home/user/build_paths"

    assert os.path.isfile(source_path), f"C source file {source_path} is missing."
    assert os.path.isfile(exec_path), f"Compiled executable {exec_path} is missing."
    assert os.access(exec_path, os.X_OK), f"File {exec_path} is not executable."

def test_output_jsonl_exists_and_correct():
    """Verify that the output JSONL file exists and contains the correct hierarchical data."""
    output_path = "/home/user/output_docs.jsonl"

    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_data = [
        {"id": 1, "name": "Electronics", "path": ["Electronics"]},
        {"id": 2, "name": "Computers", "path": ["Electronics", "Computers"]},
        {"id": 3, "name": "Laptops", "path": ["Electronics", "Computers", "Laptops"]},
        {"id": 4, "name": "Desktops", "path": ["Electronics", "Computers", "Desktops"]},
        {"id": 5, "name": "Home", "path": ["Home"]},
        {"id": 6, "name": "Furniture", "path": ["Home", "Furniture"]},
        {"id": 7, "name": "Chairs", "path": ["Home", "Furniture", "Chairs"]},
        {"id": 8, "name": "Tables", "path": ["Home", "Furniture", "Tables"]},
        {"id": 9, "name": "Audio", "path": ["Electronics", "Audio"]},
        {"id": 10, "name": "Headphones", "path": ["Electronics", "Audio", "Headphones"]}
    ]

    actual_data = []
    with open(output_path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual_data.append(obj)
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {line_num} in {output_path} is not valid JSON: {e}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} lines in {output_path}, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Mismatch at line {i+1}: expected {expected}, got {actual}."