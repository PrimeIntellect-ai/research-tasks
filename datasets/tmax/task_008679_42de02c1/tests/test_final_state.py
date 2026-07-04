# test_final_state.py

import os
import pytest

def test_recovered_flag():
    flag_path = "/home/user/recovered_flag.txt"
    assert os.path.exists(flag_path), f"Missing file: {flag_path}"
    assert os.path.isfile(flag_path), f"Expected a file, but got something else: {flag_path}"

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{pr0c_cmdl1n3_l34k_m4st3r}"
    assert content == expected_flag, f"Expected flag '{expected_flag}', but found '{content}' in {flag_path}"

def test_recover_source_code_exists():
    source_path = "/home/user/recover.c"
    assert os.path.exists(source_path), f"Missing C source file: {source_path}"
    assert os.path.isfile(source_path), f"Expected a file, but got something else: {source_path}"

    with open(source_path, "r") as f:
        content = f.read()
    assert len(content) > 0, f"The source file {source_path} is empty"

def test_recover_executable_exists():
    exec_path = "/home/user/recover"
    assert os.path.exists(exec_path), f"Missing compiled executable: {exec_path}"
    assert os.path.isfile(exec_path), f"Expected a file, but got something else: {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File is not executable: {exec_path}"