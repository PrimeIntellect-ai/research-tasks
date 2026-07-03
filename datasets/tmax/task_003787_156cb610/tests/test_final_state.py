# test_final_state.py

import os
import pytest

def compute_hash(data: bytes) -> int:
    """
    Computes the custom hash defined in the task.
    """
    sum_val = 0
    for byte in data:
        sum_val = (sum_val + byte) % 65535
    return sum_val

def test_forged_log_exists_and_valid():
    """
    Validates that the forged log exists, starts with the correct payload,
    is padded with 'A's, and has the correct custom hash.
    """
    filepath = "/home/user/forged_log.txt"
    assert os.path.exists(filepath), f"The forged log file {filepath} is missing."
    assert os.path.isfile(filepath), f"The path {filepath} is not a file."

    with open(filepath, 'rb') as f:
        content = f.read()

    payload = b"<script>alert('COMPROMISED')</script>"
    assert content.startswith(payload), "The forged log does not start with the exact required payload."

    # Check the hash
    hash_val = compute_hash(content)
    assert hash_val == 25000, f"The custom hash of the forged log is {hash_val}, expected 25000."

    # Check that the rest of the file consists of 'A's
    padding = content[len(payload):]
    assert all(b == 65 for b in padding), "The padding in the forged log must consist only of uppercase 'A' characters (ASCII 65)."

def test_fixed_cpp_exists():
    """
    Validates that the fixed C++ source file exists.
    """
    filepath = "/home/user/audit_generator_fixed.cpp"
    assert os.path.exists(filepath), f"The fixed C++ program {filepath} is missing."
    assert os.path.isfile(filepath), f"The path {filepath} is not a file."

def test_audit_report_exists_and_secure():
    """
    Validates that the audit report was generated and the XSS payload is safely HTML-encoded.
    """
    filepath = "/home/user/audit_report.html"
    assert os.path.exists(filepath), f"The audit report {filepath} is missing."
    assert os.path.isfile(filepath), f"The path {filepath} is not a file."

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Check for proper HTML encoding of the payload
    expected_encoded_payload = "&lt;script&gt;alert('COMPROMISED')&lt;/script&gt;"
    assert expected_encoded_payload in content, "The audit report does not contain the properly HTML-encoded payload."
    assert "<script>" not in content, "The audit report contains raw '<script>' tags, indicating the XSS vulnerability is not fixed."

    # Check for required wrapping tags
    assert "<body><p>" in content, "The audit report is missing the required opening <body><p> tags."
    assert "</p></body>" in content, "The audit report is missing the required closing </p></body> tags."