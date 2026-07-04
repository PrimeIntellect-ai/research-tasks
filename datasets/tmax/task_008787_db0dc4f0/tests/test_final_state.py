# test_final_state.py

import os
import stat
import pytest

def test_server_fixed_go():
    file_path = "/home/user/server_fixed.go"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read()

    # Check for XSS fix
    assert "html.EscapeString" in content, "The file does not use html.EscapeString to prevent XSS."

    # Check for Insecure Cookies fix
    assert "HttpOnly" in content and "true" in content, "The cookie does not have HttpOnly set to true."
    assert "Secure" in content and "true" in content, "The cookie does not have Secure set to true."

    # Check for CSP header
    assert "Content-Security-Policy" in content, "The Content-Security-Policy header is not set."
    assert "default-src 'self'" in content, "The Content-Security-Policy header value does not contain 'default-src 'self''."

def test_analyze_sh():
    file_path = "/home/user/analyze.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    # Check if executable
    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {file_path} is not executable."

def test_compromised_ips():
    file_path = "/home/user/compromised_ips.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run your script?"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ips = ["10.0.0.5", "192.168.1.11"]

    assert lines == expected_ips, f"Expected IPs {expected_ips}, but got {lines}."