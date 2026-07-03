# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest

REPORT_PATH = "/home/user/rotation_report.json"
BACKUP_PATH = "/home/user/backup.tar.gz"
NEW_CERT_PATH = "/home/user/new_cert.pem"
NEW_KEY_PATH = "/home/user/new_key.pem"
EXPECTED_OLD_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

def test_report_exists_and_valid_json():
    """Test that the rotation report exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report not found at {REPORT_PATH}"
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "old_pinned_hash" in data, "Missing 'old_pinned_hash' in report."
    assert "new_cert_hash" in data, "Missing 'new_cert_hash' in report."
    assert "backup_integrity_hash" in data, "Missing 'backup_integrity_hash' in report."

def test_old_pinned_hash():
    """Test that the old pinned hash is correctly extracted."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    assert data["old_pinned_hash"] == EXPECTED_OLD_HASH, "old_pinned_hash does not match expected value."

def test_backup_integrity_hash():
    """Test that the backup integrity hash is correct."""
    assert os.path.isfile(BACKUP_PATH), f"Backup file not found at {BACKUP_PATH}"

    sha256 = hashlib.sha256()
    with open(BACKUP_PATH, "rb") as f:
        sha256.update(f.read())
    expected_backup_hash = sha256.hexdigest()

    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert data["backup_integrity_hash"] == expected_backup_hash, "backup_integrity_hash is incorrect."

def test_new_certificate_generated_and_hash_correct():
    """Test that the new certificate is generated correctly and its DER hash matches the report."""
    assert os.path.isfile(NEW_CERT_PATH), f"New certificate not found at {NEW_CERT_PATH}"
    assert os.path.isfile(NEW_KEY_PATH), f"New private key not found at {NEW_KEY_PATH}"

    # Calculate DER hash using openssl
    result = subprocess.run(
        ["openssl", "x509", "-in", NEW_CERT_PATH, "-outform", "DER"],
        capture_output=True,
        check=True
    )
    der_bytes = result.stdout
    expected_cert_hash = hashlib.sha256(der_bytes).hexdigest()

    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert data["new_cert_hash"] == expected_cert_hash, "new_cert_hash does not match the actual DER hash of the new certificate."

def test_new_certificate_subject():
    """Test that the new certificate has the correct Common Name."""
    result = subprocess.run(
        ["openssl", "x509", "-noout", "-subject", "-in", NEW_CERT_PATH],
        capture_output=True,
        text=True,
        check=True
    )
    subject = result.stdout.strip()
    assert "CN = secure.example.com" in subject or "CN=secure.example.com" in subject, f"Certificate subject does not contain CN=secure.example.com. Subject: {subject}"