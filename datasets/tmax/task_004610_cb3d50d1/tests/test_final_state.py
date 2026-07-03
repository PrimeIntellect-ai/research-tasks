# test_final_state.py

import os
import subprocess
import pytest
import gzip

def test_decrypted_backup():
    backup_path = "/home/user/backup.tar.gz"
    assert os.path.isfile(backup_path), f"Decrypted backup not found at {backup_path}"

    # Check if it's a valid gzip file (tar.gz)
    try:
        with gzip.open(backup_path, 'rb') as f:
            f.read(1)
    except Exception as e:
        pytest.fail(f"File {backup_path} is not a valid gzip file: {e}")

def test_ssh_hardening():
    priv_key_path = "/home/user/.ssh/id_ed25519"
    pub_key_path = "/home/user/.ssh/id_ed25519.pub"
    config_path = "/home/user/.ssh/config"

    assert os.path.isfile(priv_key_path), f"SSH private key not found at {priv_key_path}"
    assert os.path.isfile(pub_key_path), f"SSH public key not found at {pub_key_path}"
    assert os.path.isfile(config_path), f"SSH config not found at {config_path}"

    with open(config_path, 'r') as f:
        config_content = f.read()

    assert "PasswordAuthentication no" in config_content, "SSH config does not disable PasswordAuthentication"
    assert "IdentityFile " in config_content and "id_ed25519" in config_content, "SSH config does not specify the new IdentityFile"

def test_tls_certificate():
    cert_path = "/home/user/server.crt"
    key_path = "/home/user/server.key"

    assert os.path.isfile(cert_path), f"TLS certificate not found at {cert_path}"
    assert os.path.isfile(key_path), f"TLS private key not found at {key_path}"

    # Check Common Name using openssl
    result = subprocess.run(
        ["openssl", "x509", "-noout", "-subject", "-in", cert_path],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to read certificate: {result.stderr}"
    assert "CN = internal.corp" in result.stdout or "CN=internal.corp" in result.stdout, "Certificate Common Name is not 'internal.corp'"

def test_log_sanitization_script():
    script_path = "/home/user/filter_logs.sh"
    assert os.path.isfile(script_path), f"Log sanitization script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_failed = []
    evil_failed = []

    # Test clean corpus (should preserve all lines)
    if os.path.isdir(clean_dir):
        for filename in os.listdir(clean_dir):
            filepath = os.path.join(clean_dir, filename)
            if not os.path.isfile(filepath):
                continue

            with open(filepath, 'r') as f:
                expected_output = f.read()

            result = subprocess.run(["bash", script_path, filepath], capture_output=True, text=True)
            if result.stdout != expected_output:
                clean_failed.append(filename)

    # Test evil corpus (should reject all lines)
    if os.path.isdir(evil_dir):
        for filename in os.listdir(evil_dir):
            filepath = os.path.join(evil_dir, filename)
            if not os.path.isfile(filepath):
                continue

            result = subprocess.run(["bash", script_path, filepath], capture_output=True, text=True)
            if result.stdout.strip() != "":
                evil_failed.append(filename)

    error_msg = []
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} evil files bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} clean files modified: {', '.join(clean_failed)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))