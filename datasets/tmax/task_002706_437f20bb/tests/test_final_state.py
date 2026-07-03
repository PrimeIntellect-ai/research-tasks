# test_final_state.py

import os
import hashlib
import pytest

INTEL_FILE = "/home/user/IR_case/intel.txt"
HASH_FILE = "/home/user/IR_case/hash.txt"
EXPLOIT_FILE = "/home/user/IR_case/exploit.c"
CLIENT_CERT_DIR = "/home/user/IR_case/client"

def test_intel_file_extracted():
    """Verify that the intel file was successfully dropped by the exploit."""
    assert os.path.isfile(INTEL_FILE), f"Intel file is missing at {INTEL_FILE}. The exploit may not have succeeded or the file was not created."

    with open(INTEL_FILE, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{mTLS_and_mem_corrupt_master}"
    assert content == expected_flag, f"Content of {INTEL_FILE} is incorrect. Expected '{expected_flag}', got '{content}'."

def test_hash_file_matches_intel():
    """Verify that the hash file exists and correctly matches the SHA-256 of the intel file."""
    assert os.path.isfile(INTEL_FILE), f"Cannot compute expected hash because {INTEL_FILE} is missing."
    assert os.path.isfile(HASH_FILE), f"Hash file is missing at {HASH_FILE}."

    # Derive the expected hash dynamically from the actual intel file content
    with open(INTEL_FILE, "rb") as f:
        intel_data = f.read()
    expected_hash = hashlib.sha256(intel_data).hexdigest()

    with open(HASH_FILE, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The hash in {HASH_FILE} does not match the SHA-256 hash of {INTEL_FILE}. Expected {expected_hash}, got {actual_hash}."

def test_exploit_source_exists_and_valid():
    """Verify that the student wrote the exploit.c file containing necessary components."""
    assert os.path.isfile(EXPLOIT_FILE), f"Exploit source code is missing at {EXPLOIT_FILE}."

    with open(EXPLOIT_FILE, "r") as f:
        content = f.read()

    assert "main" in content, f"{EXPLOIT_FILE} does not appear to be a valid C program (missing 'main' function)."

    # Check for basic networking or OpenSSL indicators as required by the prompt
    has_ssl = "SSL_" in content or "openssl" in content.lower()
    has_socket = "socket" in content or "connect" in content
    assert has_ssl or has_socket, f"{EXPLOIT_FILE} does not appear to contain OpenSSL or socket code required to connect to the C2 server."

def test_client_certificates_generated():
    """Verify that the student generated the required client certificates."""
    client_key = os.path.join(CLIENT_CERT_DIR, "client.key")
    client_crt = os.path.join(CLIENT_CERT_DIR, "client.crt")

    assert os.path.isfile(client_key), f"Client private key is missing at {client_key}."
    assert os.path.isfile(client_crt), f"Client certificate is missing at {client_crt}."