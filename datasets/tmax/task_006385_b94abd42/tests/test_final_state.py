# test_final_state.py

import os
import re
import subprocess
import pytest

INCIDENT_DIR = "/home/user/incident_response"

def test_phase1_log_redaction():
    redacted_log_path = os.path.join(INCIDENT_DIR, "access_redacted.log")
    assert os.path.isfile(redacted_log_path), f"Redacted log file not found at {redacted_log_path}"

    with open(redacted_log_path, "r") as f:
        content = f.read()

    # Check that sensitive data is removed
    assert "Secret123Password" not in content, "The original password was not redacted from the log."
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in content, "The original Bearer token was not redacted from the log."

    # Check that REDACTED placeholders are present
    assert "password=REDACTED" in content, "The string 'password=REDACTED' was not found in the redacted log."
    assert "Bearer REDACTED" in content, "The string 'Bearer REDACTED' was not found in the redacted log."

def test_phase2_config_rotation():
    new_enc_path = os.path.join(INCIDENT_DIR, "config_new.enc")
    assert os.path.isfile(new_enc_path), f"New encrypted config not found at {new_enc_path}"

    # Try to decrypt the new config
    decrypt_cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-pass", "pass:SecureRotation_456",
        "-in", new_enc_path
    ]

    try:
        result = subprocess.run(decrypt_cmd, capture_output=True, text=True, check=True)
        decrypted_content = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decrypt {new_enc_path} with the new password. OpenSSL error: {e.stderr}")

    assert "DB_PASSWORD=NewSecureDbPass2024!" in decrypted_content, "The new database password was not found in the decrypted configuration."
    assert "OldCompromisedDBPass!" not in decrypted_content, "The old compromised database password is still present in the configuration."

def test_phase3_ssh_hardening():
    sshd_config_path = os.path.join(INCIDENT_DIR, "sshd_config")
    assert os.path.isfile(sshd_config_path), f"sshd_config not found at {sshd_config_path}"

    with open(sshd_config_path, "r") as f:
        lines = f.readlines()

    # Strip whitespace and check active directives
    active_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

    assert "PermitRootLogin no" in active_lines, "Directive 'PermitRootLogin no' is not active in sshd_config."
    assert "PasswordAuthentication no" in active_lines, "Directive 'PasswordAuthentication no' is not active in sshd_config."

    # Ensure conflicting yes directives are removed
    assert not any(re.match(r"^PermitRootLogin\s+yes$", line) for line in active_lines), "'PermitRootLogin yes' is still active."
    assert not any(re.match(r"^PasswordAuthentication\s+yes$", line) for line in active_lines), "'PasswordAuthentication yes' is still active."

def test_phase3_ssh_key_rotation():
    key_path = os.path.join(INCIDENT_DIR, "new_keys/id_ed25519")
    assert os.path.isfile(key_path), f"New SSH private key not found at {key_path}"

    # Verify it's a valid ED25519 key
    try:
        result = subprocess.run(["ssh-keygen", "-l", "-f", key_path], capture_output=True, text=True, check=True)
        output = result.stdout.upper()
        assert "ED25519" in output, f"The generated key is not an ED25519 key. ssh-keygen output: {output}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read the SSH key with ssh-keygen. It might be invalid or have incorrect permissions. Error: {e.stderr}")