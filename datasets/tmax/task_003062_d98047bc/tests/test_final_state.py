# test_final_state.py

import os
import difflib
import pytest

def test_recovered_traffic_metric():
    """Check that the recovered traffic log matches the expected text with high similarity."""
    expected = "GET /admin/dashboard HTTP/1.1\r\nHost: internal.corp\r\nCookie: auth_token=admin_bypass_9921; role=superuser\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
    target_file = "/home/user/recovered_traffic.log"

    assert os.path.exists(target_file), f"File not found: {target_file}"

    with open(target_file, "r") as f:
        actual = f.read()

    ratio = difflib.SequenceMatcher(None, expected, actual).ratio()
    threshold = 0.95
    assert ratio >= threshold, f"String similarity metric {ratio:.4f} is below the threshold of {threshold}. Actual content: {repr(actual)}"

def test_malicious_cookie():
    """Check that the malicious cookie was correctly identified."""
    target_file = "/home/user/malicious_cookie.txt"
    expected_cookie = "Cookie: auth_token=admin_bypass_9921; role=superuser"

    assert os.path.exists(target_file), f"File not found: {target_file}"

    with open(target_file, "r") as f:
        actual = f.read().strip()

    assert expected_cookie in actual, f"Expected cookie not found in {target_file}. Found: {actual}"

def test_sandbox_output():
    """Check that the sandbox successfully isolated the process and captured its initial output."""
    target_file = "/home/user/sandbox_output.txt"

    assert os.path.exists(target_file), f"File not found: {target_file}"

    with open(target_file, "r") as f:
        actual = f.read()

    assert "Probe started." in actual, f"Expected initial output 'Probe started.' not found in {target_file}."
    assert "Error:" not in actual, f"Sandbox failed to kill the process on illegal syscall. Output contained: {actual}"