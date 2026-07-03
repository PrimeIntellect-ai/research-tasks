# test_final_state.py

import os
import stat
import pytest

def test_recovered_id_rsa_content():
    recovered_path = "/home/user/recovered_id_rsa"
    target_path = "/home/user/.ssh/target_key"

    assert os.path.exists(recovered_path), f"Missing file: {recovered_path}"
    assert os.path.exists(target_path), f"Missing original target key: {target_path}"

    with open(recovered_path, "rb") as f:
        recovered_data = f.read()

    with open(target_path, "rb") as f:
        target_data = f.read()

    assert recovered_data == target_data, f"The contents of {recovered_path} do not match the original decrypted key."

def test_recovered_id_rsa_permissions():
    recovered_path = "/home/user/recovered_id_rsa"
    assert os.path.exists(recovered_path), f"Missing file: {recovered_path}"

    st = os.stat(recovered_path)
    # Check if permissions are 0600 or 0400 (standard for private keys)
    mode = stat.S_IMODE(st.st_mode)
    assert mode in (0o600, 0o400), f"Incorrect permissions for {recovered_path}. Expected 0600 or 0400, got {oct(mode)}"

def test_isolated_run_log_content():
    log_path = "/home/user/isolated_run.log"
    assert os.path.exists(log_path), f"Missing file: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    expected_success_msg = "SUCCESS: Target payload authenticated. Attempting phone home..."
    expected_network_msg = "Network unreachable. Exiting."

    assert expected_success_msg in content, f"Log file missing expected success message. Did the script receive the correct key?"
    assert expected_network_msg in content, f"Log file missing network unreachable message. Was the network properly unshared with bwrap?"

def test_hardened_authorized_keys():
    hardened_path = "/home/user/hardened_authorized_keys"
    pub_key_path = "/home/user/.ssh/target_key.pub"

    assert os.path.exists(hardened_path), f"Missing file: {hardened_path}"
    assert os.path.exists(pub_key_path), f"Missing original public key: {pub_key_path}"

    with open(pub_key_path, "r") as f:
        pub_key_content = f.read().strip()

    # The public key usually has 3 parts: type, base64, comment. We need the type and base64 part.
    pub_key_parts = pub_key_content.split()
    assert len(pub_key_parts) >= 2, "Invalid original public key format"
    pub_key_core = f"{pub_key_parts[0]} {pub_key_parts[1]}"

    with open(hardened_path, "r") as f:
        hardened_content = f.read().strip()

    expected_prefix = 'no-pty,no-port-forwarding,command="/bin/false"'

    assert hardened_content.startswith(expected_prefix), f"File {hardened_path} does not start with the required security options."
    assert pub_key_core in hardened_content, f"File {hardened_path} does not contain the correct public key data."

    # Check that there is a space between the options and the key
    assert hardened_content.startswith(f"{expected_prefix} {pub_key_parts[0]}"), f"File {hardened_path} is not correctly formatted with a space between options and the key type."