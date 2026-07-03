# test_final_state.py

import os
import stat
import subprocess
import hashlib
import pytest

def test_cwe_report():
    """Verify that cwe_report.txt contains the correct CWE ID."""
    report_path = "/home/user/audit_app/cwe_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    with open(report_path, "r") as f:
        first_line = f.readline().strip()

    assert first_line == "CWE-134", f"Expected CWE-134 in {report_path}, found: {first_line}"

def test_logger_code_fix():
    """Verify that logger.cpp has been fixed to prevent the format string vulnerability."""
    code_path = "/home/user/audit_app/logger.cpp"
    assert os.path.isfile(code_path), f"File {code_path} is missing."

    with open(code_path, "r") as f:
        content = f.read()

    # The vulnerable pattern was exactly: snprintf(buffer, sizeof(buffer), argv[1]);
    # A correct fix would include a format string, e.g., snprintf(buffer, sizeof(buffer), "%s", argv[1]);
    assert "snprintf(buffer, sizeof(buffer), argv[1]);" not in content, \
        "The vulnerable snprintf call is still present in logger.cpp."
    assert "%s" in content, "The fix should utilize a safe format string like '%s'."

def test_secure_audit_permissions():
    """Verify that secure_audit.enc has exactly 0400 permissions."""
    enc_path = "/home/user/audit_app/secure_audit.enc"
    assert os.path.isfile(enc_path), f"File {enc_path} is missing."

    file_stat = os.stat(enc_path)
    permissions = stat.S_IMODE(file_stat.st_mode)

    assert permissions == 0o400, f"Expected permissions 0400 for {enc_path}, but got {oct(permissions)}."

def test_raw_audit_deleted():
    """Verify that the plaintext raw_audit.log has been deleted."""
    raw_path = "/home/user/audit_app/raw_audit.log"
    assert not os.path.exists(raw_path), f"Plaintext log {raw_path} still exists and was not deleted."

def test_encryption_correctness():
    """Verify that secure_audit.enc decrypts to the expected plaintext using the derived key and IV."""
    enc_path = "/home/user/audit_app/secure_audit.enc"
    assert os.path.isfile(enc_path), f"File {enc_path} is missing."

    # Derive the key
    token = "COMPLIANCE_TOKEN_2024"
    key = hashlib.sha256(token.encode('utf-8')).hexdigest()
    iv = "00000000000000000000000000000000"

    # Decrypt using openssl
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-d",
        "-in", enc_path,
        "-K", key,
        "-iv", iv
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        decrypted_text = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decrypt {enc_path}. Openssl error: {e.stderr}")

    expected_content = "USER_ACTION: Admin logged in\n"
    assert decrypted_text == expected_content, \
        f"Decrypted content did not match. Expected '{expected_content}', got '{decrypted_text}'"