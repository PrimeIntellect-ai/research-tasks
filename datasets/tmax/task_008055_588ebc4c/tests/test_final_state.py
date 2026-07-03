# test_final_state.py
import os
import stat
import pytest

def test_certs_directory_exists_and_permissions():
    path = "/home/user/certs"
    assert os.path.isdir(path), f"Directory {path} does not exist."

    st = os.stat(path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o700, f"Directory {path} has permissions {oct(mode)}, expected 0o700."

def test_cert_and_key_files_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

def test_run_exploit_script_exists():
    path = "/home/user/run_exploit.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."

def test_loot_file_exists_and_permissions():
    path = "/home/user/loot.txt"
    assert os.path.isfile(path), f"Loot file {path} does not exist."

    st = os.stat(path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o600, f"Loot file {path} has permissions {oct(mode)}, expected 0o600."

def test_loot_file_content():
    path = "/home/user/loot.txt"
    assert os.path.isfile(path), f"Loot file {path} does not exist."

    expected_content = (
        "User profile information:\n"
        "Name: John Doe\n"
        "Role: Administrator\n"
        "Account: XXXX-XXXX-XXXX-XXXX\n"
        "API_KEY: 8f92j-29eu2-9283h\n"
        "Account2: XXXX-XXXX-XXXX-XXXX"
    )

    with open(path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, "The content of loot.txt does not match the expected redacted output."