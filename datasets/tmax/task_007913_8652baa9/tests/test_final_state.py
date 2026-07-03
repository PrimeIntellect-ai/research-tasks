# test_final_state.py

import os
import json
import pytest

BUILD_ENV_DIR = "/home/user/build_env"
GO_SOURCE = os.path.join(BUILD_ENV_DIR, "migrate_and_merge.go")
GO_EXEC = os.path.join(BUILD_ENV_DIR, "migrate_and_merge")
PY_OUTPUT = os.path.join(BUILD_ENV_DIR, "py_output.json")
GO_OUTPUT = os.path.join(BUILD_ENV_DIR, "go_output.json")
DIFF_OUTPUT = os.path.join(BUILD_ENV_DIR, "verification_diff.txt")

def test_go_source_exists():
    assert os.path.isfile(GO_SOURCE), f"Go source file {GO_SOURCE} does not exist."
    with open(GO_SOURCE, 'r') as f:
        content = f.read()
    assert "package main" in content, f"{GO_SOURCE} does not appear to be a valid Go program."

def test_go_executable_exists():
    assert os.path.isfile(GO_EXEC), f"Go executable {GO_EXEC} does not exist."
    assert os.access(GO_EXEC, os.X_OK), f"{GO_EXEC} is not executable."

def test_output_files_exist():
    assert os.path.isfile(PY_OUTPUT), f"Python output file {PY_OUTPUT} does not exist."
    assert os.path.isfile(GO_OUTPUT), f"Go output file {GO_OUTPUT} does not exist."

def test_verification_diff_empty():
    assert os.path.isfile(DIFF_OUTPUT), f"Diff output file {DIFF_OUTPUT} does not exist."
    assert os.path.getsize(DIFF_OUTPUT) == 0, f"{DIFF_OUTPUT} is not empty, indicating a difference between Go and Python outputs."

def test_go_output_content():
    assert os.path.isfile(GO_OUTPUT), f"Go output file {GO_OUTPUT} does not exist."

    with open(GO_OUTPUT, 'r') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"{GO_OUTPUT} is not valid JSON.")

    expected_data = [
        {"id": "pkg-epsilon", "timestamp": 1670000050, "size_kb": 1, "schema_version": 2},
        {"id": "pkg-delta", "timestamp": 1670000050, "size_kb": 10, "schema_version": 2},
        {"id": "pkg-beta", "timestamp": 1670000075, "size_kb": 5, "schema_version": 2},
        {"id": "pkg-alpha", "timestamp": 1670000100, "size_kb": 2, "schema_version": 2},
        {"id": "pkg-gamma", "timestamp": 1670000100, "size_kb": 4, "schema_version": 2}
    ]

    assert data == expected_data, f"The parsed JSON in {GO_OUTPUT} does not match the expected migrated and sorted output."

    # Check for 2-space indentation by comparing with Python's json.dumps
    expected_str = json.dumps(expected_data, indent=2)
    assert content.strip() == expected_str.strip(), f"The formatting of {GO_OUTPUT} does not exactly match the expected 2-space indented JSON output."