# test_final_state.py

import os
import json
import subprocess
import re
import pytest

REPORT_PATH = "/home/user/forensics_report.json"
MALWARE_PATH = "/home/user/forensics/malware_agent"
ENC_PAYLOAD_PATH = "/home/user/forensics/exfiltrated.enc"
DEC_PAYLOAD_PATH = "/home/user/forensics/exfiltrated.dec"

def get_actual_key():
    """Extracts the encryption key directly from the ELF binary."""
    dump_path = "/tmp/test_c2_key.bin"
    try:
        subprocess.run(
            ["objcopy", "--dump-section", f".c2_key={dump_path}", MALWARE_PATH],
            check=True,
            capture_output=True
        )
        with open(dump_path, "rb") as f:
            key_bytes = f.read()
        return key_bytes
    finally:
        if os.path.exists(dump_path):
            os.remove(dump_path)

def decrypt_payload(key_bytes):
    """Decrypts the exfiltrated payload using the extracted key."""
    with open(ENC_PAYLOAD_PATH, "rb") as f:
        ciphertext = f.read()

    plaintext = bytearray()
    key_len = len(key_bytes)
    for i in range(len(ciphertext)):
        plaintext.append(ciphertext[i] ^ key_bytes[i % key_len])

    return plaintext.decode('utf-8', errors='ignore')

def get_expected_fingerprint(plaintext):
    """Extracts the certificate from the plaintext and calculates its SHA256 fingerprint."""
    match = re.search(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", plaintext, re.DOTALL)
    if not match:
        raise ValueError("Could not find certificate in decrypted payload")

    cert_pem = match.group(0)
    cert_path = "/tmp/test_cert.pem"
    try:
        with open(cert_path, "w") as f:
            f.write(cert_pem)

        result = subprocess.run(
            ["openssl", "x509", "-in", cert_path, "-noout", "-fingerprint", "-sha256"],
            check=True,
            capture_output=True,
            text=True
        )
        # Output format: sha256 Fingerprint=DE:AD:BE:EF...
        return result.stdout.strip().split('=')[1]
    finally:
        if os.path.exists(cert_path):
            os.remove(cert_path)

def get_expected_sqli(plaintext):
    """Finds the SQL injection payload line in the plaintext."""
    for line in plaintext.splitlines():
        if "UNION SELECT" in line:
            return line.strip()
    raise ValueError("Could not find SQLi payload in decrypted payload")

@pytest.fixture(scope="module")
def truth_data():
    """Derives all ground truth data from the initial environment state."""
    key_bytes = get_actual_key()
    key_hex = key_bytes.hex()

    plaintext = decrypt_payload(key_bytes)
    fingerprint = get_expected_fingerprint(plaintext)
    sqli_payload = get_expected_sqli(plaintext)

    return {
        "c2_key_hex": key_hex,
        "cert_fingerprint_sha256": fingerprint,
        "sqli_payload": sqli_payload
    }

@pytest.fixture(scope="module")
def student_report():
    """Loads the student's generated JSON report."""
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"
    with open(REPORT_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {REPORT_PATH} is not valid JSON.")

def test_decrypted_file_exists():
    assert os.path.exists(DEC_PAYLOAD_PATH), f"Decrypted file missing at {DEC_PAYLOAD_PATH}"
    assert os.path.getsize(DEC_PAYLOAD_PATH) > 0, f"Decrypted file at {DEC_PAYLOAD_PATH} is empty"

def test_report_c2_key(student_report, truth_data):
    assert "c2_key_hex" in student_report, "Key 'c2_key_hex' missing from report"
    assert student_report["c2_key_hex"] == truth_data["c2_key_hex"], \
        f"Incorrect C2 Key. Expected {truth_data['c2_key_hex']}, got {student_report['c2_key_hex']}"

def test_report_cert_fingerprint(student_report, truth_data):
    assert "cert_fingerprint_sha256" in student_report, "Key 'cert_fingerprint_sha256' missing from report"
    assert student_report["cert_fingerprint_sha256"] == truth_data["cert_fingerprint_sha256"], \
        f"Incorrect Certificate Fingerprint. Expected {truth_data['cert_fingerprint_sha256']}, got {student_report['cert_fingerprint_sha256']}"

def test_report_sqli_payload(student_report, truth_data):
    assert "sqli_payload" in student_report, "Key 'sqli_payload' missing from report"
    assert student_report["sqli_payload"] == truth_data["sqli_payload"], \
        f"Incorrect SQLi Payload. Expected '{truth_data['sqli_payload']}', got '{student_report['sqli_payload']}'"