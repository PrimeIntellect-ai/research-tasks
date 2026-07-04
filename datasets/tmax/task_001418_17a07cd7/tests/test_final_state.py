# test_final_state.py

import os
import json
import re
import pytest

C_FILE_PATH = "/home/user/process_backup.c"
EXEC_FILE_PATH = "/home/user/process_backup"
JSON_FILE_PATH = "/home/user/region_salaries.json"

def test_c_file_exists_and_content():
    assert os.path.isfile(C_FILE_PATH), f"C source file {C_FILE_PATH} does not exist."

    with open(C_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    assert re.search(r'NOT\s+INDEXED', content, re.IGNORECASE), \
        "The C program does not contain the 'NOT INDEXED' clause as required."

    assert re.search(r'sqlite3_bind', content, re.IGNORECASE), \
        "The C program does not appear to use 'sqlite3_bind' for parameterized queries."

def test_executable_exists():
    assert os.path.isfile(EXEC_FILE_PATH), f"Executable {EXEC_FILE_PATH} does not exist."
    assert os.access(EXEC_FILE_PATH, os.X_OK), f"File {EXEC_FILE_PATH} is not executable."

def test_json_output_correctness():
    assert os.path.isfile(JSON_FILE_PATH), f"JSON output file {JSON_FILE_PATH} does not exist."

    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON file {JSON_FILE_PATH}: {e}")

    expected_data = [
        {"region": "EU", "total_salary": 170000},
        {"region": "NA", "total_salary": 210000},
        {"region": "SA", "total_salary": 75000}
    ]

    assert isinstance(data, list), "JSON output must be a list of objects."
    assert data == expected_data, f"JSON data mismatch. Expected {expected_data}, but got {data}."