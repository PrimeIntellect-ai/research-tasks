# test_final_state.py

import os
import pytest

def test_pass_flag_exists():
    flag_path = "/home/user/project/pass.flag"
    assert os.path.isfile(flag_path), f"Expected flag file {flag_path} does not exist. The test_all.sh script may not have completed successfully."

def test_resolution_txt():
    res_path = "/home/user/resolution.txt"
    assert os.path.isfile(res_path), f"Expected report file {res_path} does not exist."

    with open(res_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != ""]

    assert len(lines) >= 3, f"Expected at least 3 lines in {res_path}, found {len(lines)}."

    file_crash = lines[0]
    syscall = lines[1]
    func_name = lines[2]

    assert file_crash == "/home/user/inputs/input_037.dat", f"Line 1: Expected '/home/user/inputs/input_037.dat', got '{file_crash}'."
    assert syscall in ("openat", "open"), f"Line 2: Expected 'openat' or 'open', got '{syscall}'."
    assert func_name == "parse_record", f"Line 3: Expected 'parse_record', got '{func_name}'."