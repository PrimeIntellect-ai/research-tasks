# test_final_state.py

import os
import re
import pytest

def test_dump_bin_extracted():
    path = "/home/user/dump.bin"
    assert os.path.isfile(path), f"File {path} does not exist. Did you extract the section?"

def test_processor_c_exists():
    path = "/home/user/processor.c"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_redacted_traffic_log():
    path = "/home/user/redacted_traffic.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Check that redaction was applied
    assert "XXXXXXXXXXXXXXXX" in content, "Credit card redaction (16 X's) not found in the output."
    assert "SSN: XXX-XX-XXXX" in content, "SSN redaction (SSN: XXX-XX-XXXX) not found in the output."

    # Check that no unredacted data remains
    unredacted_cc = re.search(r'\b\d{16}\b', content)
    assert not unredacted_cc, f"Found unredacted 16-digit credit card number in {path}."

    unredacted_ssn = re.search(r'SSN: \d{3}-\d{2}-\d{4}', content)
    assert not unredacted_ssn, f"Found unredacted SSN in {path}."

def test_certs_directory():
    path = "/home/user/certs"
    assert os.path.isdir(path), f"Directory {path} does not exist."

    # Check if there are .pem files inside
    pem_files = [f for f in os.listdir(path) if f.endswith(".pem")]
    assert len(pem_files) > 0, "No .pem files found in /home/user/certs/."

def test_cppcheck_log():
    path = "/home/user/cppcheck.log"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_valid_certs_log():
    path = "/home/user/valid_certs.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "2", f"Expected valid_certs.log to contain '2', but got '{content}'."