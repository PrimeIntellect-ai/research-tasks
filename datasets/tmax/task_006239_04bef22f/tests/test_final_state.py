# test_final_state.py

import os
import subprocess
import pytest

def test_modulus_file_correct():
    modulus_file = "/home/user/modulus.txt"
    server_crt = "/home/user/certs/server.crt"

    assert os.path.isfile(modulus_file), f"File {modulus_file} does not exist"
    assert os.path.isfile(server_crt), f"File {server_crt} does not exist (setup issue)"

    # Compute the expected modulus MD5 hash from the server certificate
    modulus_cmd = ["openssl", "x509", "-noout", "-modulus", "-in", server_crt]
    modulus_proc = subprocess.run(modulus_cmd, capture_output=True, text=True, check=True)
    modulus_output = modulus_proc.stdout.strip()

    # The output is like "Modulus=..." or similar. We need to hash it.
    md5_cmd = ["openssl", "md5"]
    md5_proc = subprocess.run(md5_cmd, input=modulus_output + "\n", capture_output=True, text=True, check=True)

    # The output of openssl md5 is usually "(stdin)= hash" or just "hash" depending on version.
    # We can just parse the hex string from the output.
    md5_output = md5_proc.stdout.strip()
    expected_hash = md5_output.split()[-1]

    with open(modulus_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_hash, f"Modulus hash in {modulus_file} is incorrect. Expected {expected_hash}, got {actual_content}"

def test_redacted_key_correct():
    redacted_file = "/home/user/redacted.key"

    assert os.path.isfile(redacted_file), f"File {redacted_file} does not exist"

    expected_content = (
        "-----BEGIN RSA PRIVATE KEY-----\n"
        "REDACTED\n"
        "-----END RSA PRIVATE KEY-----"
    )

    with open(redacted_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Redacted key in {redacted_file} is improperly formatted."