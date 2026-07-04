# test_final_state.py

import os
import json
import subprocess
import pytest

def test_forensics_report():
    report_path = "/home/user/forensics_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    cwe = report.get("vulnerability_cwe", "").upper()
    assert cwe in ["CWE-22", "CWE-23"], f"Incorrect CWE identified in report: {cwe}"

    attacker_key = report.get("attacker_public_key", "")
    assert "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKX9" in attacker_key, "Attacker public key not correctly identified in report."

    evidence = report.get("recovered_evidence", "")
    assert evidence == "flag{bash_f0r3ns1cs_p4th_tr4v3rsal}", "Recovered evidence is incorrect."

def test_poc_execution():
    poc_path = "/home/user/poc.sh"
    target_file = "/home/user/.ssh/pwned.txt"
    assert os.path.isfile(poc_path), f"PoC script {poc_path} is missing."

    # Ensure target file doesn't exist before running PoC
    if os.path.exists(target_file):
        os.remove(target_file)

    try:
        subprocess.run(["bash", poc_path], timeout=5, capture_output=True)
    except subprocess.TimeoutExpired:
        pytest.fail("PoC script execution timed out.")

    assert os.path.isfile(target_file), "PoC script failed to create the target file via path traversal."

def test_ssh_keys():
    priv_key = "/home/user/.ssh/id_ed25519"
    pub_key = "/home/user/.ssh/id_ed25519.pub"
    auth_keys = "/home/user/.ssh/authorized_keys"

    assert os.path.isfile(priv_key), f"Private key {priv_key} is missing."
    assert os.path.isfile(pub_key), f"Public key {pub_key} is missing."
    assert os.path.isfile(auth_keys), f"Authorized keys file {auth_keys} is missing."

    with open(pub_key, "r") as f:
        new_pub_key_content = f.read().strip()

    with open(auth_keys, "r") as f:
        auth_keys_content = f.read()

    assert new_pub_key_content in auth_keys_content, "Newly generated ed25519 public key not found in authorized_keys."
    assert "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKX9" not in auth_keys_content, "Attacker's key was not removed from authorized_keys."

def test_sshd_config():
    config_path = "/home/user/sshd_config_custom"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, "r") as f:
        lines = f.readlines()

    permit_root = False
    password_auth = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            key, val = parts[0].lower(), parts[1].lower()
            if key == "permitrootlogin":
                assert val == "no", f"PermitRootLogin is set to {val}, expected 'no'."
                permit_root = True
            elif key == "passwordauthentication":
                assert val == "no", f"PasswordAuthentication is set to {val}, expected 'no'."
                password_auth = True

    assert permit_root, "PermitRootLogin directive missing from sshd_config_custom."
    assert password_auth, "PasswordAuthentication directive missing from sshd_config_custom."

def test_patched_server():
    server_path = "/home/user/upload_server_patched.sh"
    assert os.path.isfile(server_path), f"Patched server script {server_path} is missing."
    assert os.access(server_path, os.X_OK), f"Patched server script {server_path} is not executable."

    # Test path traversal neutralization
    test_input = "Filename: ../../.ssh/evil.txt\nmalicious content\n"
    target_evil_file = "/home/user/.ssh/evil.txt"

    if os.path.exists(target_evil_file):
        os.remove(target_evil_file)

    try:
        subprocess.run(["bash", server_path], input=test_input.encode(), timeout=5, capture_output=True)
    except subprocess.TimeoutExpired:
        pytest.fail("Patched server execution timed out.")

    assert not os.path.exists(target_evil_file), "Patched server is still vulnerable to path traversal."