# test_final_state.py

import os
import json
import pytest

BUILD_DIR = "/home/user/polyglot_build"

def test_directory_exists():
    """Verify that the polyglot_build directory was created."""
    assert os.path.isdir(BUILD_DIR), f"Directory {BUILD_DIR} does not exist."

def test_source_files_exist():
    """Verify that the required source files exist."""
    required_files = ["parser.cpp", "processor.py", "Makefile", "input.txt"]
    for f in required_files:
        path = os.path.join(BUILD_DIR, f)
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_executables_exist():
    """Verify that the Makefile 'all' target successfully compiled the executables."""
    for exe in ["parser_x86", "parser_arm"]:
        path = os.path.join(BUILD_DIR, exe)
        assert os.path.isfile(path), f"Executable {path} is missing. Did 'make all' run successfully?"
        assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_x86_json():
    """Verify the contents of output_x86.json."""
    output_path = os.path.join(BUILD_DIR, "output_x86.json")
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did 'make test' run successfully?"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    expected_data = [
        {"id": 1, "name": "banana", "value": 25, "arch": "x86"},
        {"id": 2, "name": "cherry", "value": 5, "arch": "x86"},
        {"id": 3, "name": "apple", "value": 25, "arch": "x86"}
    ]

    assert data == expected_data, f"Data in {output_path} does not match the expected output."

def test_output_arm_json():
    """Verify the contents of output_arm.json."""
    output_path = os.path.join(BUILD_DIR, "output_arm.json")
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did 'make test' run successfully?"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    expected_data = [
        {"id": 1, "name": "banana", "value": 25, "arch": "arm"},
        {"id": 2, "name": "cherry", "value": 5, "arch": "arm"},
        {"id": 3, "name": "apple", "value": 25, "arch": "arm"}
    ]

    assert data == expected_data, f"Data in {output_path} does not match the expected output."