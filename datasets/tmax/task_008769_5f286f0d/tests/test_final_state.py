# test_final_state.py

import os
import re
import pytest

def test_cwe_finding():
    path = "/home/user/cwe_finding.txt"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read().strip().upper()

    valid_cwes = {"CWE-120", "CWE-119", "CWE-242"}
    assert content in valid_cwes, f"Expected one of {valid_cwes} in {path}, but found '{content}'"

def test_ddt_max():
    path = "/home/user/ddt_max.txt"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "3,1,6", f"Expected '3,1,6' in {path}, but found '{content}'"

def test_sensitive_data_redaction():
    clean_log_path = "/home/user/clean_requests.log"
    assert os.path.isfile(clean_log_path), f"File not found: {clean_log_path}"

    with open(clean_log_path, "r") as f:
        content = f.read()

    # Check that the specific credit card numbers are gone
    assert "4111222233334444" not in content, "Original 16-digit credit card number was not redacted"
    assert "5555666677778888" not in content, "Original 16-digit credit card number was not redacted"

    # Check that [REDACTED] is present in the expected locations
    assert "CreditCard: [REDACTED]" in content, "Expected 'CreditCard: [REDACTED]' in the cleaned log"
    assert "CC: [REDACTED], Expiry: 12/25" in content, "Expected 'CC: [REDACTED], Expiry: 12/25' in the cleaned log"

    # Verify no other 16-digit sequences exist just to be sure
    sixteen_digits = re.findall(r'\b\d{16}\b', content)
    assert len(sixteen_digits) == 0, f"Found unredacted 16-digit numbers in the cleaned log: {sixteen_digits}"