# test_final_state.py

import os
import stat
import hashlib
import pytest

def test_decrypted_files_exist():
    """Verify that the backup was successfully decrypted and extracted."""
    assert os.path.exists("/home/user/ssh_backup.tar.gz"), "Decrypted tarball /home/user/ssh_backup.tar.gz is missing."
    assert os.path.exists("/home/user/backup/deploy_keys.py"), "Extracted deploy_keys.py is missing from /home/user/backup/."

def test_deploy_keys_script_fixed():
    """Verify that the deploy_keys.py script no longer uses vulnerable os.system calls."""
    script_path = "/home/user/backup/deploy_keys.py"
    with open(script_path, "r") as f:
        content = f.read()

    # The original vulnerable script used os.system. A proper fix should use shutil or subprocess without shell=True.
    assert "os.system" not in content, "The script still contains vulnerable os.system calls."
    assert "shell=True" not in content, "The script still contains vulnerable shell=True execution."

def test_private_key_permissions():
    """Verify that the generated private key has the correct hardened permissions (600)."""
    key_path = "/home/user/new_key"
    assert os.path.exists(key_path), f"Private key not found at {key_path}"

    file_stat = os.stat(key_path)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o600, f"Private key permissions should be 0o600, but found {oct(permissions)}"

def calculate_leading_zeros(pubkey_path):
    """Helper function to calculate leading zeros of the base64 public key body."""
    try:
        with open(pubkey_path, 'r') as f:
            content = f.read().strip()
        parts = content.split()
        if len(parts) >= 2 and parts[0] == "ssh-ed25519":
            key_body = parts[1]
        else:
            key_body = parts[0]

        sha256_hex = hashlib.sha256(key_body.encode('ascii')).hexdigest()

        count = 0
        for char in sha256_hex:
            if char == '0':
                count += 1
            else:
                break
        return count
    except Exception:
        return 0

def test_vanity_key_metric():
    """Verify that the generated public key meets the vanity fingerprint requirement."""
    pubkey_path = "/home/user/new_key.pub"
    assert os.path.exists(pubkey_path), f"Public key not found at {pubkey_path}"

    metric_value = calculate_leading_zeros(pubkey_path)
    threshold = 5

    assert metric_value >= threshold, (
        f"Vanity key requirement not met. "
        f"Expected >= {threshold} leading zeros in SHA256 hash, but got {metric_value}."
    )

def test_key_deployed():
    """Verify that the new public key was deployed to the secure directory."""
    deployed_path = "/var/secure_keys/new_key.pub"
    source_path = "/home/user/new_key.pub"

    assert os.path.exists(deployed_path), f"Deployed key not found at {deployed_path}"

    with open(source_path, 'r') as f1, open(deployed_path, 'r') as f2:
        assert f1.read() == f2.read(), "The deployed key does not match the generated public key."