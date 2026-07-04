# test_final_state.py

import os
import sys
import subprocess
import datetime
import pytest

def calculate_f1(truth_set, extracted_set):
    true_positives = len(truth_set.intersection(extracted_set))
    if true_positives == 0:
        return 0.0
    precision = true_positives / len(extracted_set)
    recall = true_positives / len(truth_set)
    return 2 * (precision * recall) / (precision + recall)

def test_token_extraction_f1_score():
    """Verify that the extracted tokens meet the F1 score threshold."""
    truth = {"aB9xLp2QzM4vN7cY", "Kk3jH8fP5wR1tG6u", "7dE4sW2xZ9vC1bM0", "Xm5yN8pQ3rT6kV2j", "9fL4cV1bN7mZ3xK8"}
    token_file = "/home/user/leaked_tokens.txt"

    assert os.path.exists(token_file), f"Token file not found at {token_file}"

    with open(token_file, "r") as f:
        extracted = set([line.strip() for line in f.readlines() if line.strip()])

    f1_score = calculate_f1(truth, extracted)
    assert f1_score >= 0.85, f"F1 score {f1_score:.2f} is below the threshold of 0.85. Extracted: {extracted}"

def test_audit_script_exists():
    """Verify that the audit script exists and is executable."""
    script_path = "/home/user/audit_and_rotate.sh"
    assert os.path.exists(script_path), f"Audit script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Audit script at {script_path} is not executable"

@pytest.mark.parametrize("port", [8084, 8087])
def test_rotated_certificates(port):
    """Verify that certificates were generated with the correct specifications for vulnerable ports."""
    cert_path = f"/home/user/certs/port_{port}_cert.pem"
    key_path = f"/home/user/certs/port_{port}_key.pem"

    assert os.path.exists(cert_path), f"Certificate not found at {cert_path}"
    assert os.path.exists(key_path), f"Private key not found at {key_path}"

    # Check Common Name (CN)
    subject_out = subprocess.check_output(["openssl", "x509", "-in", cert_path, "-subject", "-noout"], text=True)
    assert "CN = service.internal" in subject_out or "CN=service.internal" in subject_out, \
        f"Certificate for port {port} does not have CN=service.internal. Subject: {subject_out.strip()}"

    # Check 2048-bit RSA key
    key_out = subprocess.check_output(["openssl", "rsa", "-in", key_path, "-text", "-noout"], text=True)
    assert "Private-Key: (2048 bit" in key_out, f"Private key for port {port} is not a 2048-bit RSA key."

    # Check 14 days validity
    dates_out = subprocess.check_output(["openssl", "x509", "-in", cert_path, "-dates", "-noout"], text=True)
    dates = {}
    for line in dates_out.strip().split('\n'):
        if '=' in line:
            key, val = line.split('=', 1)
            dates[key] = val

    assert "notBefore" in dates and "notAfter" in dates, "Could not parse certificate dates."

    # Parse dates (e.g., "May 10 23:59:59 2024 GMT")
    date_format = "%b %d %H:%M:%S %Y %Z"
    not_before = datetime.datetime.strptime(dates["notBefore"], date_format)
    not_after = datetime.datetime.strptime(dates["notAfter"], date_format)

    delta = not_after - not_before
    assert delta.days == 14, f"Certificate validity is {delta.days} days, expected exactly 14 days."