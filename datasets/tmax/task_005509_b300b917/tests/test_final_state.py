# test_final_state.py

import os
import pytest

def test_analyze_leak_script_exists():
    path = "/home/user/analyze_leak.sh"
    assert os.path.isfile(path), f"FAIL: Expected bash script {path} is missing."

def test_extract_record_executable_exists():
    path = "/home/user/extract_record"
    assert os.path.isfile(path), f"FAIL: Expected executable {path} is missing. The C program was not compiled."
    assert os.access(path, os.X_OK), f"FAIL: {path} is not executable."

def test_leak_root_cause_file_exists_and_content():
    path = "/home/user/leak_root_cause.txt"
    assert os.path.isfile(path), f"FAIL: Expected output file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "CRITICAL_LEAK_IN_SESSION_MANAGER_0x88A1"
    assert content == expected, f"FAIL: Incorrect content in {path}. Expected '{expected}', got '{content}'."