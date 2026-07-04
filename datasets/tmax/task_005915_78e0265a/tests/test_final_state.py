# test_final_state.py

import os
import pytest

def test_audit_c_exists():
    file_path = '/home/user/audit.c'
    assert os.path.isfile(file_path), f"Source file {file_path} is missing."

def test_audit_executable_exists():
    file_path = '/home/user/audit'
    assert os.path.isfile(file_path), f"Executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_vulnerable_pii_txt_correct():
    file_path = '/home/user/vulnerable_pii.txt'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ['7', '13']
    assert lines == expected_lines, f"Content of {file_path} is incorrect. Expected {expected_lines}, got {lines}."