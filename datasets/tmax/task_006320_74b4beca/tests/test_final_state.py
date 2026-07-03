# test_final_state.py

import os
import stat
import subprocess
import pytest

CERT_PATH = "/home/user/certs/new_cert.pem"
KEY_PATH = "/home/user/certs/new_key.pem"
FINGERPRINT_PATH = "/home/user/rotated_fingerprint.txt"
EXPECTED_CN = "secops.internal.rotator.v1"

def test_files_exist():
    assert os.path.exists(CERT_PATH), f"Certificate file {CERT_PATH} is missing."
    assert os.path.isfile(CERT_PATH), f"{CERT_PATH} is not a file."

    assert os.path.exists(KEY_PATH), f"Private key file {KEY_PATH} is missing."
    assert os.path.isfile(KEY_PATH), f"{KEY_PATH} is not a file."

    assert os.path.exists(FINGERPRINT_PATH), f"Fingerprint file {FINGERPRINT_PATH} is missing."
    assert os.path.isfile(FINGERPRINT_PATH), f"{FINGERPRINT_PATH} is not a file."

def test_permissions():
    key_stat = os.stat(KEY_PATH)
    cert_stat = os.stat(CERT_PATH)

    key_perms = stat.S_IMODE(key_stat.st_mode)
    cert_perms = stat.S_IMODE(cert_stat.st_mode)

    assert key_perms == 0o600, f"Expected {KEY_PATH} permissions to be 600, but got {oct(key_perms)}."
    assert cert_perms == 0o644, f"Expected {CERT_PATH} permissions to be 644, but got {oct(cert_perms)}."

def test_certificate_cn():
    try:
        result = subprocess.run(
            ["openssl", "x509", "-in", CERT_PATH, "-noout", "-subject"],
            capture_output=True, text=True, check=True
        )
        subject = result.stdout.strip()
        # The output format can vary, but it should contain the expected CN
        assert EXPECTED_CN in subject, f"Expected CN '{EXPECTED_CN}' not found in certificate subject: {subject}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read certificate subject: {e.stderr}")

def test_fingerprint_match():
    try:
        result = subprocess.run(
            ["openssl", "x509", "-in", CERT_PATH, "-noout", "-fingerprint", "-sha256"],
            capture_output=True, text=True, check=True
        )
        expected_fingerprint = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to generate certificate fingerprint: {e.stderr}")

    with open(FINGERPRINT_PATH, "r") as f:
        actual_fingerprint = f.read().strip()

    assert actual_fingerprint == expected_fingerprint, (
        f"Fingerprint in {FINGERPRINT_PATH} does not match the certificate's actual fingerprint.\n"
        f"Expected: {expected_fingerprint}\n"
        f"Got: {actual_fingerprint}"
    )