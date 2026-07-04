# test_final_state.py

import os
import json
import pytest

def test_api_test_log_content():
    log_path = "/home/user/api_test.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you save the curl output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Try to parse as JSON to handle minor formatting differences (e.g., spaces)
    try:
        parsed_content = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON: {content}")

    expected = [15, 23, 99]
    assert parsed_content == expected, f"Expected {expected} in {log_path}, but got {parsed_content}"

def test_safehashed_binary_exists():
    binary_path = "/home/user/project/safehashed"
    assert os.path.isfile(binary_path), f"Executable {binary_path} does not exist. Did the build succeed?"
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_libchecksum_so_exists():
    lib_path = "/home/user/project/libchecksum.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did the build succeed?"