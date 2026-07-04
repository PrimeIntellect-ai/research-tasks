# test_final_state.py

import os
import subprocess
import pytest

def test_cracker_files_exist():
    """Verify that the student created and compiled the C cracker program."""
    c_file = "/home/user/cracker.c"
    executable = "/home/user/cracker"

    assert os.path.isfile(c_file), f"The C source file is missing at {c_file}."
    assert os.path.isfile(executable), f"The compiled executable is missing at {executable}."
    assert os.access(executable, os.X_OK), f"The file at {executable} is not executable."

def test_csr_exists():
    """Verify that the CSR file was generated at the correct location."""
    csr_path = "/home/user/server.csr"
    assert os.path.isfile(csr_path), f"The Certificate Signing Request file is missing at {csr_path}."

def test_csr_subject():
    """Verify that the generated CSR contains the exact required Subject details."""
    csr_path = "/home/user/server.csr"

    result = subprocess.run(
        ["openssl", "req", "-in", csr_path, "-noout", "-subject"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to read CSR subject. OpenSSL error: {result.stderr}"

    subject = result.stdout.strip()

    # Check for the required fields in the subject output
    assert "C = US" in subject or "C=US" in subject, f"Country (C) is not 'US' in the CSR subject. Actual subject: {subject}"
    assert "O = SecCorp" in subject or "O=SecCorp" in subject, f"Organization (O) is not 'SecCorp' in the CSR subject. Actual subject: {subject}"
    assert "CN = internal.seccorp.local" in subject or "CN=internal.seccorp.local" in subject, f"Common Name (CN) is not 'internal.seccorp.local' in the CSR subject. Actual subject: {subject}"

def test_csr_signature_verification():
    """Verify that the CSR is valid and correctly signed by the private key."""
    csr_path = "/home/user/server.csr"

    result = subprocess.run(
        ["openssl", "req", "-in", csr_path, "-noout", "-verify"],
        capture_output=True,
        text=True
    )

    # OpenSSL outputs "verify OK" to stderr or stdout depending on the version, and returns 0 on success.
    assert result.returncode == 0, f"CSR signature verification failed. The CSR may be malformed or not signed properly. OpenSSL error: {result.stderr}"

    output = result.stdout + result.stderr
    assert "verify OK" in output, "CSR verification did not indicate success ('verify OK' not found in output)."