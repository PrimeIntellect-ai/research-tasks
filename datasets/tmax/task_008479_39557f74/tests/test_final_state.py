# test_final_state.py

import os
import base64
import hmac
import hashlib
import pytest

def get_expected_token():
    """Derive the expected token based on the truth data."""
    user = base64.urlsafe_b64encode(b"admin").rstrip(b'=')
    role = base64.urlsafe_b64encode(b"superuser").rstrip(b'=')
    message = user + b"." + role
    key = b"S3cur1ty_H@rdc0d3d_99!"
    mac = hmac.new(key, message, hashlib.sha256).digest()
    mac_b64 = base64.urlsafe_b64encode(mac).rstrip(b'=')
    return (message + b"." + mac_b64).decode('utf-8')

def test_flag_file_correct():
    """Verify that the flag file exists and contains the correct flag."""
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Flag file {flag_path} does not exist."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{h4rdc0d3d_s3cr3ts_r_b4d}"
    assert content == expected_flag, f"Flag file content '{content}' does not match expected '{expected_flag}'."

def test_forged_token_file_correct():
    """Verify that the forged token file exists and contains the correct token."""
    token_path = "/home/user/forged_token.txt"
    assert os.path.isfile(token_path), f"Token file {token_path} does not exist."

    with open(token_path, "r") as f:
        content = f.read().strip()

    expected_token = get_expected_token()
    assert content == expected_token, f"Token file content '{content}' does not match expected '{expected_token}'."

def test_forge_go_exists_and_non_empty():
    """Verify that the forge.go script exists and has content."""
    script_path = "/home/user/forge.go"
    assert os.path.isfile(script_path), f"Go script {script_path} does not exist."
    assert os.path.getsize(script_path) > 0, f"Go script {script_path} is empty."