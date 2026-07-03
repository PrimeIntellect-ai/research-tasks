# test_final_state.py

import os
import re
import pytest

def test_redacted_secrets_file():
    """
    Validates that the redacted_secrets.txt file exists and contains the correctly sanitized data.
    Credit card numbers must be replaced with [REDACTED].
    """
    file_path = "/home/user/redacted_secrets.txt"
    assert os.path.isfile(file_path), f"Verification Failed: {file_path} not found."

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    expected_content = (
        "User: Alice Dept: HR CC: [REDACTED]\n"
        "User: Bob Dept: IT CC: [REDACTED]\n"
        "User: Charlie Dept: Sales ID: 99823\n"
        "User: Dave Dept: Exec CC: [REDACTED]"
    )

    assert actual_content == expected_content, (
        f"Verification Failed: {file_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )

def test_nginx_block_conf():
    """
    Validates that the nginx_block.conf file exists and contains the correct block directives.
    Only IPs with more than 3 HTTP 403 responses should be blocked.
    """
    file_path = "/home/user/nginx_block.conf"
    assert os.path.isfile(file_path), f"Verification Failed: {file_path} not found."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Based on the access.log, 10.0.0.5 has 4 403s, 172.16.0.2 has 2 403s.
    # So only 10.0.0.5 should be denied.
    expected_directive = "deny 10.0.0.5;"

    assert expected_directive in lines, (
        f"Verification Failed: {file_path} does not contain the expected directive '{expected_directive}'."
    )

    # Ensure no other IPs were incorrectly blocked
    for line in lines:
        if line.startswith("deny "):
            ip = line.replace("deny ", "").replace(";", "").strip()
            assert ip == "10.0.0.5", f"Verification Failed: IP {ip} was incorrectly blocked in {file_path}."