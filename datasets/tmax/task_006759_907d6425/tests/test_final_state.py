# test_final_state.py

import os
import json
import pytest

def test_logs_extracted():
    logs_dir = "/home/user/logs"
    assert os.path.exists(logs_dir), f"Expected directory {logs_dir} to exist."
    assert os.path.isdir(logs_dir), f"Expected {logs_dir} to be a directory."

    log1 = os.path.join(logs_dir, "backup_1.log")
    log2 = os.path.join(logs_dir, "backup_2.log")
    assert os.path.exists(log1), f"Expected {log1} to be extracted."
    assert os.path.exists(log2), f"Expected {log2} to be extracted."

def test_parser_c_exists():
    c_file = "/home/user/parser.c"
    assert os.path.exists(c_file), f"Expected C source file {c_file} to exist."
    assert os.path.isfile(c_file), f"Expected {c_file} to be a file."

def test_parser_executable_exists():
    executable = "/home/user/parser"
    assert os.path.exists(executable), f"Expected compiled executable {executable} to exist."
    assert os.path.isfile(executable), f"Expected {executable} to be a file."
    assert os.access(executable, os.X_OK), f"Expected {executable} to be executable."

def test_output_json_exists_and_correct():
    output_file = "/home/user/failed_jobs.json"
    assert os.path.exists(output_file), f"Expected output file {output_file} to exist."
    assert os.path.isfile(output_file), f"Expected {output_file} to be a file."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {output_file}, but found {len(lines)}."

    parsed_objects = []
    for line in lines:
        try:
            parsed_objects.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line in {output_file} is not valid JSON: {line}")

    expected_objects = [
        {"JobID": 102, "Status": "FAILED", "Files": 12},
        {"JobID": 201, "Status": "FAILED", "Files": 100}
    ]

    # Sort both lists by JobID to compare regardless of order
    parsed_objects.sort(key=lambda x: x.get("JobID", 0))
    expected_objects.sort(key=lambda x: x["JobID"])

    assert parsed_objects == expected_objects, f"Contents of {output_file} do not match expected JSON objects."