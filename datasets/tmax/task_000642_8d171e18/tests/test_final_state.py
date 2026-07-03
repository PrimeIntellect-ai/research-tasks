# test_final_state.py
import os
import subprocess
import re
import pytest

def test_audit_port():
    sshd_config_path = "/home/user/investigation/sshd_config"
    audit_port_path = "/home/user/audit_port.txt"

    assert os.path.exists(audit_port_path), f"{audit_port_path} does not exist."

    # Derive the expected port
    expected_port = None
    with open(sshd_config_path, "r") as f:
        ports = [line.split()[1] for line in f if line.startswith("Port ")]
        # The secondary port is the one that is not 22
        for p in set(ports):
            if p != "22":
                expected_port = p
                break

    assert expected_port is not None, "Could not find a secondary port in sshd_config."

    with open(audit_port_path, "r") as f:
        actual_port = f.read().strip()

    assert actual_port == expected_port, f"Expected port {expected_port} in {audit_port_path}, but found {actual_port}."

def test_audit_key():
    auth_keys_path = "/home/user/investigation/authorized_keys"
    audit_key_path = "/home/user/audit_key.txt"

    assert os.path.exists(audit_key_path), f"{audit_key_path} does not exist."

    # Derive the expected key comment
    expected_comment = None
    with open(auth_keys_path, "r") as f:
        for line in f:
            if line.startswith("ssh-dss "):
                parts = line.strip().split()
                if len(parts) >= 3:
                    expected_comment = parts[2]
                break

    assert expected_comment is not None, "Could not find ssh-dss key comment in authorized_keys."

    with open(audit_key_path, "r") as f:
        actual_comment = f.read().strip()

    assert actual_comment == expected_comment, f"Expected key comment {expected_comment} in {audit_key_path}, but found {actual_comment}."

def test_validator_c_fixed():
    validator_c_path = "/home/user/investigation/validator.c"

    assert os.path.exists(validator_c_path), f"{validator_c_path} does not exist."

    with open(validator_c_path, "r") as f:
        content = f.read()

    # Check that the vulnerability is fixed
    # X509_verify_cert returns 1 on success
    assert "result >= 0" not in content, "The vulnerability (result >= 0) is still present in validator.c."
    assert "result == 1" in content or "1 == result" in content, "The fix (result == 1) was not found in validator.c."

def test_validator_compiled():
    validator_bin_path = "/home/user/investigation/validator"
    assert os.path.exists(validator_bin_path), f"Compiled binary {validator_bin_path} does not exist."
    assert os.access(validator_bin_path, os.X_OK), f"Compiled binary {validator_bin_path} is not executable."

def test_valid_token_file():
    valid_token_path = "/home/user/valid_token_file.txt"
    tokens_dir = "/home/user/investigation/tokens"
    ca_path = "/home/user/investigation/ca.pem"

    assert os.path.exists(valid_token_path), f"{valid_token_path} does not exist."

    # Derive the expected valid token using openssl verify
    expected_token = None
    for token_file in os.listdir(tokens_dir):
        if not token_file.endswith(".pem"):
            continue
        token_path = os.path.join(tokens_dir, token_file)
        result = subprocess.run(
            ["openssl", "verify", "-CAfile", ca_path, token_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "OK" in result.stdout:
            expected_token = token_file
            break

    assert expected_token is not None, "Could not find a valid token signed by the CA."

    with open(valid_token_path, "r") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_token, f"Expected valid token {expected_token} in {valid_token_path}, but found {actual_token}."