# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_audit_report_json():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Audit report {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert data.get("extracted_hash") == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "Incorrect extracted_hash in audit report."
    assert data.get("cracked_password") == "test", "Incorrect cracked_password in audit report."
    assert data.get("ssh_key_type") == "ed25519", "Incorrect ssh_key_type in audit report."
    assert data.get("crafted_payload") == "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAtest", "Incorrect crafted_payload in audit report."

def test_ssh_key_exists_and_encrypted():
    key_path = "/home/user/compliance_key"
    assert os.path.exists(key_path), f"SSH private key {key_path} does not exist."
    assert os.path.isfile(key_path), f"{key_path} is not a file."

    # Verify the key is encrypted with the passphrase "test"
    result = subprocess.run(
        ["ssh-keygen", "-y", "-P", "test", "-f", key_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to decrypt SSH key. The passphrase might be incorrect or the key is invalid."
    assert "ssh-ed25519" in result.stdout, "The SSH key is not of type ed25519."

def test_ssh_permissions_and_authorized_keys():
    ssh_dir = "/home/user/.ssh"
    auth_keys_path = os.path.join(ssh_dir, "authorized_keys")
    key_path = "/home/user/compliance_key"

    assert os.path.exists(ssh_dir), f"Directory {ssh_dir} does not exist."
    assert stat.S_IMODE(os.stat(ssh_dir).st_mode) == 0o700, f"Permissions on {ssh_dir} are not 700."

    assert os.path.exists(auth_keys_path), f"File {auth_keys_path} does not exist."
    assert stat.S_IMODE(os.stat(auth_keys_path).st_mode) == 0o600, f"Permissions on {auth_keys_path} are not 600."

    # Get the public key
    result = subprocess.run(
        ["ssh-keygen", "-y", "-P", "test", "-f", key_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        pub_key = result.stdout.strip()
        with open(auth_keys_path, "r") as f:
            auth_keys_content = f.read()
        assert pub_key in auth_keys_content, "The generated public key is not present in authorized_keys."