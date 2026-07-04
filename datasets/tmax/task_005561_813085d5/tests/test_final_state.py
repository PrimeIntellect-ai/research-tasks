# test_final_state.py

import os
from pathlib import Path
import pytest

def test_flagged_ips_content():
    """Test that flagged_ips.txt contains exactly the expected unique flagged IPs."""
    flagged_ips_file = Path("/home/user/flagged_ips.txt")
    assert flagged_ips_file.is_file(), f"File not found: {flagged_ips_file}. The C++ program may not have created it."

    content = flagged_ips_file.read_text().strip().splitlines()
    actual_ips = set(line.strip() for line in content if line.strip())

    expected_ips = {"192.168.1.100", "172.16.0.50", "10.0.0.12"}

    assert actual_ips == expected_ips, f"flagged_ips.txt does not contain the correct IPs. Expected {expected_ips}, but got {actual_ips}"
    assert len(content) == len(expected_ips), "flagged_ips.txt contains duplicate entries or extra lines."

def test_weak_certs_content():
    """Test that weak_certs.txt contains exactly the paths of the weak and expired certificates."""
    weak_certs_file = Path("/home/user/weak_certs.txt")
    assert weak_certs_file.is_file(), f"File not found: {weak_certs_file}. The bash script may not have created it."

    content = weak_certs_file.read_text().strip().splitlines()
    actual_certs = set(line.strip() for line in content if line.strip())

    expected_certs = {
        "/home/user/certs/cert_expired.pem",
        "/home/user/certs/cert_weak.pem"
    }

    assert actual_certs == expected_certs, f"weak_certs.txt does not contain the correct certificate paths. Expected {expected_certs}, but got {actual_certs}"
    assert len(content) == len(expected_certs), "weak_certs.txt contains duplicate entries or extra lines."

def test_authorized_keys_hardened():
    """Test that authorized_keys no longer contains keys associated with flagged IPs."""
    auth_keys_file = Path("/home/user/.ssh/authorized_keys")
    assert auth_keys_file.is_file(), f"File not found: {auth_keys_file}"

    content = auth_keys_file.read_text().strip().splitlines()
    actual_entries = [line.strip() for line in content if line.strip()]

    # We expect only the safe IPs to remain
    expected_safe_identifiers = ["user@10.0.0.5", "user@10.0.0.8"]
    flagged_identifiers = ["192.168.1.100", "172.16.0.50", "10.0.0.12"]

    for entry in actual_entries:
        for flagged in flagged_identifiers:
            assert flagged not in entry, f"Found flagged IP {flagged} in authorized_keys. The file was not properly sanitized."

    # Check that the safe entries are still there
    found_safe_count = 0
    for entry in actual_entries:
        for safe in expected_safe_identifiers:
            if safe in entry:
                found_safe_count += 1

    assert found_safe_count == len(expected_safe_identifiers), f"authorized_keys is missing expected safe keys. Expected to find entries for {expected_safe_identifiers}."
    assert len(actual_entries) == len(expected_safe_identifiers), "authorized_keys contains unexpected extra entries."