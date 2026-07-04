# test_final_state.py

import os
import pytest
import re

def test_decrypt_rs_exists():
    """Test that the student created the decrypt.rs file."""
    path = "/home/user/decrypt.rs"
    assert os.path.isfile(path), f"Rust decryption script missing at {path}"
    assert os.path.getsize(path) > 0, f"Rust decryption script at {path} is empty"

def test_report_txt_exists():
    """Test that the report.txt file exists."""
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"Final report missing at {path}"

def test_report_txt_contents():
    """Test that the report.txt contains the correct decrypted text and CN."""
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"Final report missing at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_evidence = "Decrypted Evidence: CRITICAL_EXFIL:root_password_hash_dumped"
    expected_cn = "Attacker CN: malicious-c2.local"

    assert expected_evidence in content, "The decrypted evidence in the report is incorrect or missing."
    assert expected_cn in content, "The attacker CN in the report is incorrect or missing."

    # Ensure exact formatting of the two lines
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    evidence_found = False
    cn_found = False
    for line in lines:
        if line == expected_evidence:
            evidence_found = True
        elif line == expected_cn:
            cn_found = True

    assert evidence_found, f"Expected exact line '{expected_evidence}' not found in report.txt"
    assert cn_found, f"Expected exact line '{expected_cn}' not found in report.txt"