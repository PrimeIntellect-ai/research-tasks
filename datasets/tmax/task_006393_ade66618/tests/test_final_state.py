# test_final_state.py

import os
import stat
import pytest

HOME_DIR = "/home/user"

def test_recovered_key():
    token_path = os.path.join(HOME_DIR, "legacy_token.bin")
    recovered_key_path = os.path.join(HOME_DIR, "recovered_key.txt")

    assert os.path.isfile(token_path), f"Legacy token file missing at {token_path}"
    assert os.path.isfile(recovered_key_path), f"Recovered key file missing at {recovered_key_path}"

    # Derive the expected key dynamically
    known_plaintext = b'{"user":"admin","action":"rotate"}'
    with open(token_path, "rb") as f:
        ciphertext = f.read()

    assert len(ciphertext) >= 4, "Ciphertext is too short"

    # XOR first 4 bytes to find the key
    expected_key_bytes = bytes([ciphertext[i] ^ known_plaintext[i] for i in range(4)])
    expected_key_hex = expected_key_bytes.hex().lower()

    with open(recovered_key_path, "r") as f:
        actual_key_hex = f.read().strip().lower()

    assert actual_key_hex == expected_key_hex, f"Recovered key is incorrect. Expected {expected_key_hex}, got {actual_key_hex}"

def test_privilege_escalation_audit():
    vuln_file_path = os.path.join(HOME_DIR, "vuln_file.txt")
    script_path = os.path.join(HOME_DIR, "rotation_scripts", "rotate_keys.py")

    assert os.path.isfile(vuln_file_path), f"Vulnerable file record missing at {vuln_file_path}"

    with open(vuln_file_path, "r") as f:
        vuln_filename = f.read().strip()

    assert vuln_filename == "rotate_keys.py", f"Incorrect vulnerable file identified: {vuln_filename}"

    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    # Check permissions
    mode = os.stat(script_path).st_mode
    is_world_writable = bool(mode & stat.S_IWOTH)
    assert not is_world_writable, f"File {script_path} is still world-writable"

    # Specifically check if it was set to 755
    assert stat.S_IMODE(mode) == 0o755, f"Permissions on {script_path} should be exactly 755, but got {oct(stat.S_IMODE(mode))}"

def test_certificate_validation():
    chain_status_path = os.path.join(HOME_DIR, "chain_status.txt")

    assert os.path.isfile(chain_status_path), f"Chain status file missing at {chain_status_path}"

    with open(chain_status_path, "r") as f:
        status = f.read().strip()

    assert status == "CHAIN_OK", f"Incorrect chain status: {status}. Expected 'CHAIN_OK'"