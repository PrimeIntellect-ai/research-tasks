# test_final_state.py
import os
import pytest

def test_audit_cpp_exists():
    path = '/home/user/audit.cpp'
    assert os.path.isfile(path), f"Expected C++ source file {path} does not exist."

def test_audit_binary_exists():
    path = '/home/user/audit'
    assert os.path.isfile(path), f"Expected compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_violation_path_output():
    path = '/home/user/violation_path.txt'
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_path = "N1,N2,N3,N4,N6"
    assert content == expected_path, f"Output file {path} contains '{content}', but expected '{expected_path}'."