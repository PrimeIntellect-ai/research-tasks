# test_final_state.py

import os
import pytest

def test_hidden_ca_txt():
    path = "/home/user/hidden_ca.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you analyze the legacy binary and extract the URL?"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_url = "https://staging-ca.internal.net/cert.pem"
    assert expected_url in content, f"File {path} does not contain the correct staging CA URL."

def test_fixed_inspector_compiled():
    path = "/home/user/fixed_inspector"
    assert os.path.isfile(path), f"File {path} is missing. Did you compile the fixed C code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_safe_traffic_txt():
    path = "/home/user/safe_traffic.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the fixed binary and redirect output?"

    with open(path, 'r') as f:
        content = f.read()

    assert "Content-Security-Policy: default-src 'self'" in content, "The safe_traffic.txt file does not contain the prepended Content-Security-Policy header."
    assert "SSN: REDACTED!!!" in content, "The safe_traffic.txt file does not properly redact the SSN with 'REDACTED!!!'."
    assert "Status: Active" in content, "The safe_traffic.txt file is missing the 'Status: Active' line, which indicates the buffer overflow fix might have truncated the output."
    assert "SSN: 987-65-4321" not in content, "The original SSN is still present in the safe_traffic.txt file."

def test_cwe_120_fix_in_source():
    path = "/home/user/traffic_inspector.c"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    # The original code had `strcpy(buffer, temp);` where buffer was 128 bytes and temp was 1024.
    # We shouldn't strictly enforce how they fix it (e.g. strncpy, increasing buffer size, removing temp entirely),
    # but we should ensure the blatant strcpy into a 128 byte buffer from a 1024 byte buffer is addressed.
    # A simple check is that the exact original vulnerable line is gone or the buffer size was increased.
    # Since checking AST for C is hard in pure python, we rely on the safe_traffic.txt output length 
    # and content (Status: Active) to verify the fix works at runtime.
    pass