# test_final_state.py

import os
import subprocess
import pytest

def test_cert_and_key_exist():
    """Verify that cert.pem and key.pem exist."""
    assert os.path.isfile("/home/user/cert.pem"), "/home/user/cert.pem is missing."
    assert os.path.isfile("/home/user/key.pem"), "/home/user/key.pem is missing."

def test_cert_properties():
    """Verify the certificate is RSA 2048, CN=legacy.internal, and valid for >= 365 days."""
    # Check Common Name
    subject_cmd = ["openssl", "x509", "-in", "/home/user/cert.pem", "-noout", "-subject"]
    result = subprocess.run(subject_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to read cert.pem: {result.stderr}"
    assert "CN = legacy.internal" in result.stdout or "CN=legacy.internal" in result.stdout, "Certificate Common Name is not 'legacy.internal'."

    # Check key size (RSA 2048)
    key_cmd = ["openssl", "rsa", "-in", "/home/user/key.pem", "-noout", "-text"]
    result = subprocess.run(key_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to read key.pem: {result.stderr}"
    assert "Private-Key: (2048 bit" in result.stdout, "Private key is not 2048-bit RSA."

    # Check expiration (365 days = 31536000 seconds)
    # If the cert is valid for at least 365 days from its creation, 
    # and it was just created, it should not expire within 364 days (31449600 seconds).
    exp_cmd = ["openssl", "x509", "-in", "/home/user/cert.pem", "-noout", "-checkend", "31449600"]
    result = subprocess.run(exp_cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Certificate is not valid for at least 365 days."

def test_generate_token_c_exists():
    """Verify that generate_token.c exists."""
    assert os.path.isfile("/home/user/generate_token.c"), "/home/user/generate_token.c is missing."

def test_token_txt_properties():
    """Verify token.txt exists, is 16 chars long, and has no newline."""
    assert os.path.isfile("/home/user/token.txt"), "/home/user/token.txt is missing."
    with open("/home/user/token.txt", "rb") as f:
        content = f.read()

    assert len(content) == 16, f"token.txt must be exactly 16 characters long, but it is {len(content)} bytes."
    assert b"\n" not in content, "token.txt must not contain newline characters."

def test_validator_success():
    """Compile and run validator.c against the generated cert and token."""
    validator_src = "/home/user/validator.c"
    validator_bin = "/home/user/validator"
    cert_path = "/home/user/cert.pem"
    token_path = "/home/user/token.txt"

    assert os.path.isfile(validator_src), f"{validator_src} is missing."

    # Compile validator
    compile_cmd = ["gcc", validator_src, "-o", validator_bin]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compile validator.c:\n{result.stderr}"

    # Run validator
    run_cmd = [validator_bin, cert_path, token_path]
    result = subprocess.run(run_cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Validator exited with code {result.returncode}. Output: {result.stdout.strip()}"
    assert result.stdout.strip() == "VALID", f"Validator output was not 'VALID'. Output: {result.stdout.strip()}"