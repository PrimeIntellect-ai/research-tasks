# test_final_state.py

import os
import stat
import pytest

def test_decrypted_key_exists_and_permissions():
    key_path = "/home/user/id_rsa"
    assert os.path.isfile(key_path), f"Decrypted private key missing at {key_path}"

    mode = os.stat(key_path).st_mode
    # Check that group and others have no permissions (restrictive permissions)
    assert (mode & 0o077) == 0, f"Permissions on {key_path} are too open. Expected restrictive permissions (e.g., 600 or 400)."

def test_result_fingerprint_matches():
    result_path = "/home/user/result.txt"
    expected_path = "/home/user/expected_fingerprint.txt"

    assert os.path.isfile(result_path), f"Result file missing at {result_path}"
    assert os.path.isfile(expected_path), f"Expected fingerprint file missing at {expected_path}"

    with open(result_path, 'r') as f:
        result_content = f.read().strip()

    with open(expected_path, 'r') as f:
        expected_content = f.read().strip()

    assert result_content == expected_content, f"Fingerprint in {result_path} does not match the expected fingerprint."