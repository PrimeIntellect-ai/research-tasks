# test_final_state.py

import os
import re
import pytest

def get_fallback_key():
    """Extract the fallback key from the legacy binary to use as truth."""
    binary_path = "/home/user/legacy_auth"
    assert os.path.exists(binary_path), f"Binary {binary_path} is missing."
    with open(binary_path, 'rb') as f:
        content = f.read()

    match = re.search(b'FBK_[a-zA-Z0-9_]+', content)
    assert match is not None, "Could not find fallback key pattern in binary."
    return match.group(0).decode('utf-8')

def test_compromised_ips():
    """Test that compromised_ips.txt contains the correctly identified and sorted IPs."""
    log_path = "/home/user/auth_events.log"
    output_path = "/home/user/compromised_ips.txt"

    assert os.path.exists(log_path), f"Log file {log_path} is missing."
    assert os.path.exists(output_path), f"Output file {output_path} was not created."

    fallback_key = get_fallback_key()

    # Compute expected IPs
    expected_ips = set()
    with open(log_path, 'r') as f:
        for line in f:
            if 'status="SUCCESS"' in line and f'cred="{fallback_key}"' in line:
                ip_match = re.search(r'IP=([0-9\.]+)', line)
                if ip_match:
                    expected_ips.add(ip_match.group(1))

    expected_ips_sorted = sorted(list(expected_ips))

    # Read actual IPs
    with open(output_path, 'r') as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips_sorted, f"Expected IPs {expected_ips_sorted}, but got {actual_ips}"

def test_redacted_log():
    """Test that redacted_auth_events.log is correctly sanitized."""
    log_path = "/home/user/auth_events.log"
    redacted_path = "/home/user/redacted_auth_events.log"

    assert os.path.exists(log_path), f"Original log file {log_path} is missing."
    assert os.path.exists(redacted_path), f"Redacted log file {redacted_path} was not created."

    fallback_key = get_fallback_key()

    # Compute expected redacted content
    expected_lines = []
    with open(log_path, 'r') as f:
        for line in f:
            expected_lines.append(line.replace(fallback_key, '[REDACTED_CRED]'))

    # Read actual redacted content
    with open(redacted_path, 'r') as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_lines), "Redacted log does not have the same number of lines as the original log."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1} of redacted log.\nExpected: {expected.strip()}\nActual: {actual.strip()}"

def test_rust_project_exists():
    """Test that the Rust project was created in the correct location."""
    cargo_path = "/home/user/log_processor/Cargo.toml"
    assert os.path.exists(cargo_path), f"Rust Cargo project not found at {cargo_path}."
    assert os.path.isfile(cargo_path), f"{cargo_path} should be a file."