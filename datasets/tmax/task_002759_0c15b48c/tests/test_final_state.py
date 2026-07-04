# test_final_state.py

import os
import subprocess
import pytest

def test_extracted_secrets_log():
    """Verify that the extracted_secrets.log file exists and contains the correct sorted secrets."""
    log_path = '/home/user/extracted_secrets.log'
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # We determine the expected secrets by looking at the running processes, or fallback to truth
    try:
        output = subprocess.check_output(['ps', '-eo', 'command'], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command to check running processes.")

    found_secrets = set()
    for line in output.splitlines():
        if '/tmp/vuln_service' in line and '--secret' in line:
            parts = line.split()
            try:
                secret_idx = parts.index('--secret')
                if secret_idx + 1 < len(parts):
                    found_secrets.add(parts[secret_idx + 1])
            except ValueError:
                continue

    expected_secrets = sorted(list(found_secrets)) if found_secrets else ['AlphaBeta123', 'EpsilonZeta789', 'GammaDelta456']

    assert lines == expected_secrets, f"Contents of {log_path} do not match the expected sorted secrets. Expected {expected_secrets}, got {lines}."

def test_ssh_keys_exist_and_valid():
    """Verify that the Ed25519 SSH key pair exists."""
    priv_key_path = '/home/user/.ssh/ir_key'
    pub_key_path = '/home/user/.ssh/ir_key.pub'

    assert os.path.isfile(priv_key_path), f"Private key {priv_key_path} does not exist."
    assert os.path.isfile(pub_key_path), f"Public key {pub_key_path} does not exist."

    with open(pub_key_path, 'r') as f:
        pub_key_content = f.read().strip()

    assert pub_key_content.startswith('ssh-ed25519'), f"The public key {pub_key_path} is not an Ed25519 key."

def test_authorized_keys_restricted():
    """Verify that the public key is in authorized_keys with the restrict option."""
    pub_key_path = '/home/user/.ssh/ir_key.pub'
    auth_keys_path = '/home/user/.ssh/authorized_keys'

    assert os.path.isfile(auth_keys_path), f"The file {auth_keys_path} does not exist."

    with open(pub_key_path, 'r') as f:
        pub_key_content = f.read().strip()

    with open(auth_keys_path, 'r') as f:
        auth_keys_content = f.read().splitlines()

    expected_line = f"restrict {pub_key_content}"

    found = any(line.strip() == expected_line for line in auth_keys_content)
    assert found, f"The authorized_keys file does not contain the correctly restricted key entry. Expected to find exactly: '{expected_line}'"