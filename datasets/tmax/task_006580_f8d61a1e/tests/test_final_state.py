# test_final_state.py

import os
import re
import subprocess
import pytest

def test_rotation_summary():
    summary_path = "/home/user/rotation_summary.txt"
    assert os.path.isfile(summary_path), f"Missing required file: {summary_path}"

    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {summary_path}, got {len(lines)}"

    # Check IP
    assert lines[0] == "Trigger IP: 10.0.45.22", f"Line 1 incorrect: {lines[0]}"

    # Check checksum
    checksum_path = "/home/user/checksums.txt"
    assert os.path.isfile(checksum_path), f"Missing {checksum_path}"
    with open(checksum_path, "r") as f:
        expected_checksum = f.read().split()[0]

    assert lines[1] == f"Old Key Checksum: {expected_checksum}", f"Line 2 incorrect: {lines[1]}"

    # Check CN
    assert lines[2] == "New Cert CN: rotated.local", f"Line 3 incorrect: {lines[2]}"

def test_new_credentials_valid_rsa():
    key_path = "/home/user/new_credentials.pem"
    assert os.path.isfile(key_path), f"Missing required file: {key_path}"

    # Use openssl to verify the key
    result = subprocess.run(["openssl", "rsa", "-in", key_path, "-check", "-noout"], capture_output=True, text=True)
    assert result.returncode == 0, f"Invalid RSA key in {key_path}: {result.stderr}"

def test_new_cert_valid():
    cert_path = "/home/user/new_cert.pem"
    assert os.path.isfile(cert_path), f"Missing required file: {cert_path}"

    # Verify it's a valid cert
    result = subprocess.run(["openssl", "x509", "-in", cert_path, "-noout", "-subject"], capture_output=True, text=True)
    assert result.returncode == 0, f"Invalid certificate in {cert_path}: {result.stderr}"

    # Check CN
    assert "CN" in result.stdout and "rotated.local" in result.stdout, f"Certificate does not have correct CN: {result.stdout}"

def test_cert_matches_key():
    key_path = "/home/user/new_credentials.pem"
    cert_path = "/home/user/new_cert.pem"

    # Get modulus of key
    key_mod = subprocess.run(["openssl", "rsa", "-noout", "-modulus", "-in", key_path], capture_output=True, text=True).stdout.strip()
    # Get modulus of cert
    cert_mod = subprocess.run(["openssl", "x509", "-noout", "-modulus", "-in", cert_path], capture_output=True, text=True).stdout.strip()

    assert key_mod, "Could not extract modulus from private key"
    assert key_mod == cert_mod, "The certificate does not match the generated private key"