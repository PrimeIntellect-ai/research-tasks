# test_final_state.py

import os
import subprocess
import pytest

def test_scripts_exist_and_executable():
    """Test that the required scripts exist and are executable."""
    scripts = [
        "/home/user/process_logs.sh",
        "/home/user/run_sandbox.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} is missing."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_sandbox_script_contents():
    """Test that run_sandbox.sh uses bwrap with required security constraints."""
    script_path = "/home/user/run_sandbox.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "bwrap" in content, "run_sandbox.sh must use bwrap."
    assert "--unshare-net" in content, "run_sandbox.sh must unshare the network namespace."
    assert "--dev" in content, "run_sandbox.sh must mount /dev."
    # We don't strictly assert the exact string "--ro-bind / /" because they might do it differently,
    # but the instructions say "entire root filesystem / must be mounted read-only" 
    # and we can check for --ro-bind.
    assert "--ro-bind" in content, "run_sandbox.sh must use --ro-bind."

def test_encrypted_file_exists():
    """Test that the encrypted audit log was generated."""
    enc_file = "/home/user/audit_trail/secure_audit.log.enc"
    assert os.path.isfile(enc_file), f"Encrypted log file {enc_file} is missing."
    assert os.path.getsize(enc_file) > 0, f"Encrypted log file {enc_file} is empty."

def test_decryption_and_redaction():
    """Test that the file can be decrypted and contains correctly redacted logs."""
    enc_file = "/home/user/audit_trail/secure_audit.log.enc"
    key_file = "/home/user/certs/audit_key.pem"
    decrypted_file = "/tmp/decrypted.log"

    # Decrypt the file
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-salt",
        "-in", enc_file,
        "-pass", f"file:{key_file}",
        "-out", decrypted_file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Decryption failed: {result.stderr}"
    assert os.path.isfile(decrypted_file), "Decrypted file was not created."

    with open(decrypted_file, "r") as f:
        content = f.read()

    # Check that sensitive data is removed
    sensitive_data = ["4555666677778888", "AKIAIOSFODNN7EXAMPLE", "SECRET_999", "1234"]
    for secret in sensitive_data:
        assert secret not in content, f"Sensitive data '{secret}' was not redacted."

    # Check that redaction markers exist
    assert "card=REDACTED" in content, "Missing 'card=REDACTED' in the logs."
    assert "api_key=REDACTED" in content, "Missing 'api_key=REDACTED' in the logs."

    # Check that benign parameters still exist
    benign_data = ["item=shoes", "format=json", "user=admin"]
    for benign in benign_data:
        assert benign in content, f"Benign parameter '{benign}' was incorrectly modified or removed."

    # Cleanup
    if os.path.exists(decrypted_file):
        os.remove(decrypted_file)