# test_final_state.py

import os
import stat
import pytest

def test_recovered_key_exists_and_content():
    key_path = "/home/user/.ssh/id_ed25519_recovered"
    assert os.path.exists(key_path), f"Recovered key file {key_path} does not exist."
    assert os.path.isfile(key_path), f"{key_path} is not a file."

    with open(key_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    assert "-----BEGIN OPENSSH PRIVATE KEY-----" in content, "The recovered key does not contain the standard OpenSSH private key header."
    assert "b3BlbnNzaC" in content, "The recovered key content does not match the expected decrypted payload."

def test_recovered_key_permissions():
    key_path = "/home/user/.ssh/id_ed25519_recovered"
    assert os.path.exists(key_path), f"Recovered key file {key_path} does not exist."

    st = os.stat(key_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Permissions for {key_path} are {oct(permissions)}, expected 0o600 (-rw-------)."

def test_cwe_finding_content():
    cwe_path = "/home/user/cwe_finding.txt"
    assert os.path.exists(cwe_path), f"CWE finding file {cwe_path} does not exist."
    assert os.path.isfile(cwe_path), f"{cwe_path} is not a file."

    with open(cwe_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().strip()

    assert content == "CWE-327", f"Expected CWE finding to be 'CWE-327', but got '{content}'."