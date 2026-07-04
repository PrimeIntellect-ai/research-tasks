# test_final_state.py

import os
import hashlib
import re
import pytest

def test_cwe_report():
    report_path = "/home/user/forensics/cwe_report.txt"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    valid_cwes = {"CWE-120", "CWE-121", "CWE-242"}
    assert content in valid_cwes, f"Expected one of {valid_cwes} in {report_path}, but found: '{content}'"

def test_network_policy_configuration():
    script_path = "/home/user/forensics/block_c2.sh"
    assert os.path.isfile(script_path), f"File not found: {script_path}"

    with open(script_path, "r") as f:
        content = f.read().strip()

    assert "iptables" in content, f"'iptables' command missing in {script_path}"
    assert "-d 203.0.113.88" in content, f"Destination IP '-d 203.0.113.88' missing in {script_path}"
    assert "-j DROP" in content, f"Action '-j DROP' missing in {script_path}"

    has_append = "-A OUTPUT" in content
    has_insert = "-I OUTPUT" in content
    assert has_append or has_insert, f"Expected '-A OUTPUT' or '-I OUTPUT' in {script_path}"

def test_sensitive_data_redaction():
    redacted_path = "/home/user/forensics/redacted_data.txt"
    assert os.path.isfile(redacted_path), f"File not found: {redacted_path}"

    expected_content = (
        "John Doe, dob: 1980-01-01, ssn: 123-45-REDACTED, balance: $5000\n"
        "Jane Smith, dob: 1992-05-15, ssn: 987-65-REDACTED, balance: $12000\n"
        "System Admin, notes: \"Call the bank about 000-11-REDACTED tomorrow.\"\n"
    )

    with open(redacted_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {redacted_path} does not match the expected redacted output."

def test_cryptographic_hashing():
    payload_path = "/home/user/forensics/malware_payload.bin"
    report_path = "/home/user/forensics/hash_report.txt"

    assert os.path.isfile(payload_path), f"File not found: {payload_path}"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(payload_path, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(report_path, "r") as f:
        content = f.read().strip()

    # Allow optional space after colon
    pattern = rf"^SHA256:\s*{expected_hash}$"
    assert re.match(pattern, content, re.IGNORECASE), f"Content of {report_path} ('{content}') does not match expected format 'SHA256: {expected_hash}'"