# test_final_state.py

import os
import stat
import pytest

COMPROMISED_KEY_1 = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcompromised1 dummy@host"
COMPROMISED_KEY_2 = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIcompromised2 dummy@host"
SAFE_KEY_1 = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsafe1 alice@host"
SAFE_KEY_2 = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIsafe2 bob@host"

def test_rotation_report():
    report_path = "/home/user/rotation_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read()

    assert "Removed compromised keys: 4" in content, "Report does not contain the correct count of removed keys (expected 4)."
    assert "Admin key generated: true" in content, "Report does not contain 'Admin key generated: true'."

def test_admin_key_permissions():
    priv_key_path = "/home/user/app_users/admin/id_ed25519"
    pub_key_path = "/home/user/app_users/admin/id_ed25519.pub"

    assert os.path.isfile(priv_key_path), f"Admin private key {priv_key_path} does not exist."
    assert os.path.isfile(pub_key_path), f"Admin public key {pub_key_path} does not exist."

    priv_mode = stat.S_IMODE(os.stat(priv_key_path).st_mode)
    pub_mode = stat.S_IMODE(os.stat(pub_key_path).st_mode)

    assert priv_mode == 0o600, f"Private key permissions should be 0600, got {oct(priv_mode)}."
    assert pub_mode == 0o644, f"Public key permissions should be 0644, got {oct(pub_mode)}."

def test_alice_authorized_keys_sanitized():
    filepath = "/home/user/app_users/alice/authorized_keys"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().splitlines()

    assert SAFE_KEY_1 in content, f"Alice's safe key was removed from {filepath}."
    assert COMPROMISED_KEY_1 not in content, f"Compromised key 1 still present in {filepath}."
    assert COMPROMISED_KEY_2 not in content, f"Compromised key 2 still present in {filepath}."

def test_bob_authorized_keys_sanitized():
    filepath = "/home/user/app_users/bob/authorized_keys"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().splitlines()

    assert SAFE_KEY_2 in content, f"Bob's safe key was removed from {filepath}."
    assert COMPROMISED_KEY_2 not in content, f"Compromised key 2 still present in {filepath}."

def test_admin_authorized_keys_updated():
    filepath = "/home/user/app_users/admin/authorized_keys"
    pub_key_path = "/home/user/app_users/admin/id_ed25519.pub"

    assert os.path.isfile(filepath), f"File {filepath} does not exist."
    assert os.path.isfile(pub_key_path), f"Admin public key {pub_key_path} does not exist."

    with open(filepath, "r") as f:
        auth_content = f.read().splitlines()

    with open(pub_key_path, "r") as f:
        pub_content = f.read().strip()

    assert COMPROMISED_KEY_1 not in auth_content, f"Compromised key 1 still present in {filepath}."
    assert pub_content in auth_content, f"Newly generated admin public key was not appended to {filepath}."