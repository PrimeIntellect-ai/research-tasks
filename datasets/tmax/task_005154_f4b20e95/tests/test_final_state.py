# test_final_state.py

import os
import subprocess
import pytest

def test_c_binary_compiled_correctly():
    path = "/home/user/artifacts/c_linux_amd64"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Test execution and output (should reverse the string)
    result = subprocess.run([path, "abcdef"], capture_output=True, text=True)
    assert result.stdout == "fedcba", f"Expected 'fedcba', but got '{result.stdout}'. Was ENABLE_REVERSE=1 passed?"

def test_go_binary_compiled_correctly():
    path = "/home/user/artifacts/go_linux_amd64"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Test execution and output
    result = subprocess.run([path, "12345"], capture_output=True, text=True)
    assert result.stdout == "54321", f"Expected '54321', but got '{result.stdout}'."

def test_go_windows_cross_compiled():
    path = "/home/user/artifacts/go_windows_amd64.exe"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Check if it's a Windows PE executable
    with open(path, "rb") as f:
        header = f.read(2)
    assert header == b"MZ", f"File {path} does not appear to be a valid Windows executable (missing MZ header)."

def test_test_report_generated():
    path = "/home/user/artifacts/test_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the tests?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert "PROPERTY TESTS PASSED" in content, f"Report file {path} does not contain the expected success message."

def test_python_script_modified():
    path = "/home/user/src/test_props.py"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "TODO: Implement subprocess calls" not in content, "The Python script still contains the TODO comment, indicating it was not fully modified."
    assert "subprocess" in content, "The Python script does not seem to use 'subprocess'."