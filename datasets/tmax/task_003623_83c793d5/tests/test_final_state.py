# test_final_state.py

import os
import hashlib

def test_auth_config_updated():
    path = "/home/user/auth_config.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    expected_hash = hashlib.sha256(b"Nova_Core_77X!S@lt_90210_X").hexdigest()

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == expected_hash, f"File {path} does not contain the expected hash. Found: {content}"

def test_rotation_log_contents():
    path = "/home/user/rotation_log.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    expected_hash = hashlib.sha256(b"Nova_Core_77X!S@lt_90210_X").hexdigest()
    expected_lines = [
        "SALT=S@lt_90210_X",
        f"HASH={expected_hash}",
        "RESULT=Access Granted"
    ]

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Expected 3 lines in {path}, found {len(lines)}"
    assert lines[0] == expected_lines[0], f"Expected first line to be '{expected_lines[0]}', found '{lines[0]}'"
    assert lines[1] == expected_lines[1], f"Expected second line to be '{expected_lines[1]}', found '{lines[1]}'"
    assert lines[2] == expected_lines[2], f"Expected third line to be '{expected_lines[2]}', found '{lines[2]}'"

def test_cpp_files_exist():
    cpp_path = "/home/user/rotate_cred.cpp"
    bin_path = "/home/user/rotate_cred"

    assert os.path.exists(cpp_path), f"Source file {cpp_path} does not exist."
    assert os.path.exists(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."