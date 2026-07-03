# test_final_state.py

import os
import stat
import pytest

def test_cert_status():
    path = "/home/user/cert_status.txt"
    assert os.path.isfile(path), f"File not found: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "VALID", f"Expected cert_status.txt to contain 'VALID', but got '{content}'"

def test_ssh_key_permissions():
    path = "/home/user/.ssh/id_rsa"
    assert os.path.isfile(path), f"File not found: {path}"

    file_stat = os.stat(path)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o600, f"Expected permissions 0600 for {path}, but got {oct(permissions)}"

def test_sym_key():
    path = "/home/user/sym.key"
    assert os.path.isfile(path), f"File not found: {path}"

    size = os.path.getsize(path)
    assert size == 32, f"Expected sym.key to be exactly 32 bytes, but got {size} bytes"

def test_decrypt_traffic_script_exists():
    path = "/home/user/decrypt_traffic.py"
    assert os.path.isfile(path), f"File not found: {path}"

def test_decrypted_payload():
    path = "/home/user/decrypted_payload.txt"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read()

    expected = "CRITICAL_PAYLOAD_DATA_XYZ_12345"
    assert content == expected, f"Expected decrypted payload to be '{expected}', but got '{content}'"