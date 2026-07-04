# test_final_state.py

import os
import hmac
import hashlib
import subprocess
import pytest

def test_audit_report_txt():
    """Verify the contents of the plain text audit report."""
    path = "/home/user/compliance/audit_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_content = "Tampered File: process_logs.sh\nVulnerability: CWE-78"
    assert content == expected_content, f"Content of {path} does not match expected output. Got:\n{content}"

def test_fixed_script():
    """Verify the fixed script exists, removes eval, and looks safe."""
    path = "/home/user/compliance/fixed_script.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "eval" not in content, "The fixed script still contains 'eval', which is unsafe."
    # It should contain ls and some variable usage
    assert "ls " in content, "The fixed script does not appear to perform the directory listing."
    assert "$1" in content or "INPUT_DIR" in content, "The fixed script does not use the input variable."

def test_audit_report_encrypted():
    """Verify the encrypted audit report can be decrypted and matches the expected text."""
    enc_path = "/home/user/compliance/audit_report.enc"
    assert os.path.isfile(enc_path), f"File {enc_path} does not exist."

    # Decrypt using openssl
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-in", enc_path,
        "-pass", "pass:AuditSafe2024"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        decrypted_content = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decrypt {enc_path}. Ensure it was encrypted with AES-256-CBC, PBKDF2, and the correct passphrase. Error: {e.stderr}")

    expected_content = "Tampered File: process_logs.sh\nVulnerability: CWE-78"
    assert decrypted_content == expected_content, f"Decrypted content does not match expected output. Got:\n{decrypted_content}"

def test_report_hmac():
    """Verify the HMAC signature of the encrypted report."""
    enc_path = "/home/user/compliance/audit_report.enc"
    hmac_path = "/home/user/compliance/report.hmac"

    assert os.path.isfile(enc_path), f"Encrypted file {enc_path} missing, cannot verify HMAC."
    assert os.path.isfile(hmac_path), f"HMAC file {hmac_path} does not exist."

    with open(enc_path, 'rb') as f:
        enc_data = f.read()

    expected_hmac = hmac.new(b"integrity_key_99", enc_data, hashlib.sha256).hexdigest()

    with open(hmac_path, 'r') as f:
        actual_hmac = f.read().strip()

    # OpenSSL dgst might output something like "HMAC-SHA256(file)= hex" or just hex if awk was used.
    # The instructions say "Extract ONLY the hex string".
    assert expected_hmac in actual_hmac, f"HMAC signature in {hmac_path} does not match the expected HMAC-SHA256 of the encrypted file."
    # Ensure it's exactly the hex string
    assert actual_hmac == expected_hmac, f"HMAC file should contain exactly the hex string. Got: {actual_hmac}"