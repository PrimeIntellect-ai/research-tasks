# test_final_state.py

import os
import re
import ssl
import urllib.request
import subprocess
import pytest

def test_secure_audit_c_exists():
    """Verify that secure_audit.c exists."""
    assert os.path.isfile("/home/user/secure_audit.c"), "/home/user/secure_audit.c does not exist."

def test_audit_key_txt_format():
    """Verify audit_key.txt exists and contains valid KEY and IV."""
    key_file = "/home/user/audit_key.txt"
    assert os.path.isfile(key_file), f"{key_file} does not exist."

    with open(key_file, "r") as f:
        content = f.read()

    key_match = re.search(r"^KEY:\s*([0-9a-fA-F]{64})$", content, re.MULTILINE)
    iv_match = re.search(r"^IV:\s*([0-9a-fA-F]{32})$", content, re.MULTILINE)

    assert key_match is not None, "KEY not found or not 64 hex characters in audit_key.txt."
    assert iv_match is not None, "IV not found or not 32 hex characters in audit_key.txt."

def test_audit_trail_enc_exists():
    """Verify audit_trail.enc exists."""
    assert os.path.isfile("/home/user/audit_trail.enc"), "/home/user/audit_trail.enc does not exist."

def test_certs_exist():
    """Verify the TLS certificates exist."""
    assert os.path.isfile("/home/user/certs/audit_cert.pem"), "/home/user/certs/audit_cert.pem does not exist."
    assert os.path.isfile("/home/user/certs/audit_key.pem"), "/home/user/certs/audit_key.pem does not exist."

def test_tls_server_and_decryption():
    """Download encrypted file via TLS, decrypt it, and compare with expected output."""
    # Download via HTTPS
    url = "https://localhost:8443/audit_trail.enc"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, context=ctx, timeout=5) as response:
            assert response.status == 200, f"HTTP status code {response.status}"
            encrypted_data = response.read()
    except Exception as e:
        pytest.fail(f"Failed to download from {url}: {e}")

    # Write downloaded data to temp file
    temp_enc = "/tmp/downloaded_audit_trail.enc"
    with open(temp_enc, "wb") as f:
        f.write(encrypted_data)

    # Extract KEY and IV
    with open("/home/user/audit_key.txt", "r") as f:
        content = f.read()
    key = re.search(r"^KEY:\s*([0-9a-fA-F]{64})$", content, re.MULTILINE).group(1)
    iv = re.search(r"^IV:\s*([0-9a-fA-F]{32})$", content, re.MULTILINE).group(1)

    # Decrypt using openssl
    temp_dec = "/tmp/decrypted_audit_trail.txt"
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-K", key, "-iv", iv,
        "-in", temp_enc, "-out", temp_dec
    ]
    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode == 0, f"Decryption failed: {result.stderr.decode()}"

    # Read decrypted data
    with open(temp_dec, "r") as f:
        decrypted_text = f.read()

    # Generate expected output
    find_cmd = "find /usr/bin -type f -perm -4000 | sort"
    find_result = subprocess.run(find_cmd, shell=True, capture_output=True, text=True)
    assert find_result.returncode == 0, "Failed to run find command for expected output."
    expected_text = find_result.stdout

    assert decrypted_text == expected_text, "Decrypted text does not match expected setuid files list."