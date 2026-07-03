# test_final_state.py
import os
import pytest

def test_solution_txt_exists_and_correct():
    path = "/home/user/solution.txt"
    assert os.path.exists(path), f"File {path} is missing. Did you redirect the output?"
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "VULNERABILITY_CONFIRMED: SQL_INJECTION_BYPASS"
    assert expected in content, f"Expected '{expected}' in {path}, but got '{content}'"

def test_trigger_cpp_exists():
    path = "/home/user/trigger.cpp"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read()

    assert "ANALYZE_DBG_" in content, f"Expected environment variable prefix 'ANALYZE_DBG_' in {path}"

def test_trigger_binary_exists():
    path = "/home/user/trigger"
    assert os.path.exists(path), f"File {path} is missing. Did you compile trigger.cpp?"
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."