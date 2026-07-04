# test_final_state.py

import os
import subprocess
import pytest

def test_authorized_keys_safe():
    """Test that authorized_keys.safe is created correctly without the attacker's key."""
    original_path = '/home/user/incident/authorized_keys'
    safe_path = '/home/user/incident/authorized_keys.safe'

    assert os.path.isfile(safe_path), f"The file {safe_path} is missing."

    with open(original_path, 'r') as f:
        original_lines = f.read().splitlines()

    with open(safe_path, 'r') as f:
        safe_lines = f.read().splitlines()

    # Find the malicious domain from the original file
    # We know from the setup it's evil-empire.xyz
    malicious_domain = "evil-empire.xyz"

    expected_lines = [line for line in original_lines if malicious_domain not in line]

    assert len(safe_lines) == len(expected_lines), f"{safe_path} should have {len(expected_lines)} lines, but has {len(safe_lines)}."
    assert safe_lines == expected_lines, f"The contents of {safe_path} do not match the expected cleaned keys (order must be preserved)."

def test_safe_redirect_binary():
    """Test the safe_redirect binary functionality."""
    binary_path = '/home/user/incident/safe_redirect'

    assert os.path.isfile(binary_path), f"The executable {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

    # Test valid URL
    valid_url = "https://safe.example.com/dashboard"
    result_valid = subprocess.run([binary_path, valid_url], capture_output=True, text=True)
    expected_valid = f"Location: {valid_url}\n\n"
    assert result_valid.stdout == expected_valid, "safe_redirect did not output correctly for a valid URL."

    # Test invalid URL
    invalid_url = "http://evil-empire.xyz/steal"
    result_invalid = subprocess.run([binary_path, invalid_url], capture_output=True, text=True)
    expected_error = "Location: https://safe.example.com/error\n\n"
    assert result_invalid.stdout == expected_error, "safe_redirect did not output correctly for an invalid URL."

    # Test no arguments
    result_no_args = subprocess.run([binary_path], capture_output=True, text=True)
    assert result_no_args.stdout == expected_error, "safe_redirect did not output correctly when no arguments were provided."

def test_csp_txt():
    """Test that csp.txt contains the correct Content Security Policy."""
    csp_path = '/home/user/incident/csp.txt'

    assert os.path.isfile(csp_path), f"The file {csp_path} is missing."

    with open(csp_path, 'r') as f:
        content = f.read().strip()

    expected_csp = "Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none';"
    assert content == expected_csp, f"The content of {csp_path} is incorrect."