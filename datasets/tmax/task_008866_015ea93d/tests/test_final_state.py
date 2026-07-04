# test_final_state.py

import os
import pytest

def test_password_extracted_correctly():
    pwd_file = "/home/user/old_password.txt"
    assert os.path.exists(pwd_file), f"File {pwd_file} does not exist."

    with open(pwd_file, "r") as f:
        content = f.read().strip()

    expected_pwd = "Str0ngL3gacyP@ssw0rd!2023"
    assert content == expected_pwd, f"The extracted password in {pwd_file} is incorrect."

def test_vulnerability_fixed_in_source():
    src_file = "/home/user/new_auth_worker.cpp"
    assert os.path.exists(src_file), f"File {src_file} does not exist."

    with open(src_file, "r") as f:
        content = f.read()

    assert "system(" not in content, "The system() call is still present in the source code."
    assert "safe_ping(" in content, "The safe_ping() function is not used in the source code."

def test_fixed_binary_compiled():
    bin_file = "/home/user/new_auth_worker_fixed"
    assert os.path.exists(bin_file), f"Compiled binary {bin_file} does not exist."
    assert os.path.isfile(bin_file), f"{bin_file} is not a file."
    assert os.access(bin_file, os.X_OK), f"Compiled binary {bin_file} is not executable."

    # Check if it's an ELF file
    with open(bin_file, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{bin_file} is not a valid ELF executable."