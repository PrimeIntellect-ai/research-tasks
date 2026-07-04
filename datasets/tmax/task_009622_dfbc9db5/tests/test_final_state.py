# test_final_state.py

import os
import stat
import pytest

def test_fetch_data_script_exists():
    script_path = "/home/user/fetch_data.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_secret_file_exists_and_content():
    secret_path = "/home/user/secret.txt"
    assert os.path.isfile(secret_path), f"The file {secret_path} was not created."

    with open(secret_path, "r") as f:
        content = f.read().strip()

    expected_content = "SEC-9988-FLAG-2023"
    assert content == expected_content, f"The content of {secret_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_secret_file_permissions():
    secret_path = "/home/user/secret.txt"
    assert os.path.isfile(secret_path), f"The file {secret_path} does not exist to check permissions."

    st = os.stat(secret_path)
    # Check if permissions are exactly 400 (-r--------)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"The file {secret_path} has incorrect permissions. Expected 0o400, got {oct(permissions)}."