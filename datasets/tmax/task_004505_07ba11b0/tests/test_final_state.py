# test_final_state.py

import os
import hashlib
import pytest

def test_xss_ips_extraction():
    """Test that XSS IPs are correctly extracted, sorted, and unique."""
    log_path = "/home/user/logs/access.log"
    output_path = "/home/user/xss_ips.txt"

    assert os.path.exists(output_path), f"File {output_path} does not exist."

    # Derive expected IPs from the log file
    expected_ips = set()
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                if "<script>" in line:
                    parts = line.split()
                    if parts:
                        expected_ips.add(parts[0])

    expected_ips_sorted = sorted(list(expected_ips))

    with open(output_path, "r") as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips_sorted, f"Expected IPs {expected_ips_sorted}, but got {actual_ips} in {output_path}."

def test_vuln_script_identification():
    """Test that the vulnerable script was correctly identified."""
    output_path = "/home/user/vuln_script.txt"
    scripts_dir = "/home/user/scripts/"

    assert os.path.exists(output_path), f"File {output_path} does not exist."

    # Derive the vulnerable script by analyzing the scripts directory
    expected_script = None
    if os.path.exists(scripts_dir):
        for filename in os.listdir(scripts_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(scripts_dir, filename)
                with open(filepath, "r") as f:
                    content = f.read()
                    if "os.system(" in content and "sys.argv" in content:
                        expected_script = filename
                        break

    if not expected_script:
        expected_script = "backup_manager.py" # fallback if setup was modified

    with open(output_path, "r") as f:
        actual_script = f.read().strip()

    assert actual_script == expected_script, f"Expected vulnerable script '{expected_script}', but got '{actual_script}' in {output_path}."

def test_audit_sha256():
    """Test that the SHA-256 hash of xss_ips.txt is correctly calculated."""
    xss_ips_path = "/home/user/xss_ips.txt"
    audit_path = "/home/user/audit.sha256"

    assert os.path.exists(audit_path), f"File {audit_path} does not exist."
    assert os.path.exists(xss_ips_path), f"File {xss_ips_path} must exist to compute its hash."

    # Recompute the hash from the actual xss_ips.txt file
    with open(xss_ips_path, "rb") as f:
        file_bytes = f.read()

    expected_hash = hashlib.sha256(file_bytes).hexdigest()

    with open(audit_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected SHA-256 hash '{expected_hash}', but got '{actual_hash}' in {audit_path}."