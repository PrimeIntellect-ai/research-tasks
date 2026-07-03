# test_final_state.py
import os
import re
import subprocess

def test_decrypted_token():
    path = "/home/user/decrypted_token.txt"
    assert os.path.exists(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_token = "AUTH_TOKEN_9a8b7c6d5e4f3g2h1"
    assert content == expected_token, f"Decrypted token is incorrect. Expected '{expected_token}', got '{content}'"

def test_key_manager_c_fixed():
    path = "/home/user/key_manager.c"
    assert os.path.exists(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "system" not in content, "The vulnerable 'system' function call is still present in key_manager.c"
    assert "fopen" in content, "The secure 'fopen' function is missing in key_manager.c"
    assert "fprintf" in content or "fputs" in content, "A secure file writing function (like fprintf or fputs) is missing in key_manager.c"
    assert "/home/user/managed_authorized_keys" in content, "The target file path '/home/user/managed_authorized_keys' is missing in key_manager.c"

def test_key_manager_executable():
    path = "/home/user/key_manager"
    assert os.path.exists(path), f"Executable not found: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File is not a valid ELF executable: {path}"

def test_sshd_config_hardened():
    path = "/home/user/sshd_config"
    assert os.path.exists(path), f"File not found: {path}"

    with open(path, "r") as f:
        lines = f.readlines()

    permit_root_login_no = False
    password_auth_no = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check PermitRootLogin
        if re.match(r"^PermitRootLogin\s+yes\b", line, re.IGNORECASE):
            assert False, "Found uncommented 'PermitRootLogin yes' in sshd_config"
        if re.match(r"^PermitRootLogin\s+no\b", line, re.IGNORECASE):
            permit_root_login_no = True

        # Check PasswordAuthentication
        if re.match(r"^PasswordAuthentication\s+yes\b", line, re.IGNORECASE):
            assert False, "Found uncommented 'PasswordAuthentication yes' in sshd_config"
        if re.match(r"^PasswordAuthentication\s+no\b", line, re.IGNORECASE):
            password_auth_no = True

    assert permit_root_login_no, "'PermitRootLogin no' is missing or commented out in sshd_config"
    assert password_auth_no, "'PasswordAuthentication no' is missing or commented out in sshd_config"