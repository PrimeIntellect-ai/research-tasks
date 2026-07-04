# test_final_state.py

import os
import subprocess
import hashlib
import re
from collections import defaultdict
import pytest

def test_cert_fingerprint_extracted_correctly():
    cert_path = "/home/user/webapp/certs/server.crt"
    output_path = "/home/user/audit/cert_fingerprint.txt"

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    # Derive expected fingerprint directly from the certificate
    try:
        cmd = ["openssl", "x509", "-noout", "-fingerprint", "-sha256", "-in", cert_path]
        expected_output = subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected certificate fingerprint: {e}")

    with open(output_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Fingerprint in {output_path} does not match the actual certificate fingerprint.\n"
        f"Expected: {expected_output}\n"
        f"Found: {actual_output}"
    )

def test_file_integrity_verification():
    checksums_path = "/home/user/webapp/checksums.txt"
    web_root_path = "/home/user/webapp/web_root"
    output_path = "/home/user/audit/tampered_files.txt"

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    # Recompute hashes to find tampered files dynamically
    expected_tampered = []
    with open(checksums_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            expected_hash, filename = line.split(maxsplit=1)
            file_path = os.path.join(web_root_path, filename)

            if not os.path.isfile(file_path):
                continue

            with open(file_path, "rb") as target_file:
                actual_hash = hashlib.sha256(target_file.read()).hexdigest()

            if actual_hash != expected_hash:
                expected_tampered.append(filename)

    with open(output_path, "r") as f:
        actual_tampered = [line.strip() for line in f if line.strip()]

    assert set(actual_tampered) == set(expected_tampered), (
        f"Tampered files list is incorrect.\n"
        f"Expected: {expected_tampered}\n"
        f"Found: {actual_tampered}"
    )

def test_sensitive_data_redaction():
    script_path = "/home/user/audit/redact.sh"
    original_log_path = "/home/user/webapp/logs/access.log"
    clean_log_path = "/home/user/audit/clean_access.log"

    assert os.path.isfile(script_path), f"Redaction script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Redaction script is not executable: {script_path}"
    assert os.path.isfile(clean_log_path), f"Cleaned log file missing: {clean_log_path}"

    # Compute the expected redacted log
    expected_lines = []
    with open(original_log_path, "r") as f:
        for line in f:
            # Redact password, token, and ssn query parameters
            redacted_line = re.sub(r'(password|token|ssn)=([^&\s]+)', r'\1=[REDACTED]', line)
            expected_lines.append(redacted_line)

    with open(clean_log_path, "r") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        "The redacted log file does not match the expected output. "
        "Ensure all 'password', 'token', and 'ssn' parameters are replaced with '[REDACTED]'."
    )

def test_network_policy_generation():
    script_path = "/home/user/audit/block_ips.sh"
    original_log_path = "/home/user/webapp/logs/access.log"

    assert os.path.isfile(script_path), f"Network policy script missing: {script_path}"

    # Parse the log to find the top 3 IPs with 404 errors
    ip_404_counts = defaultdict(int)
    with open(original_log_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) > 8 and parts[8] == "404":
                ip = parts[0]
                ip_404_counts[ip] += 1

    # Sort by count descending, take top 3
    top_ips = sorted(ip_404_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    expected_commands = [
        f"iptables -A INPUT -s {ip} -j DROP" for ip, count in top_ips
    ]

    with open(script_path, "r") as f:
        # Extract non-empty lines that aren't bash comments or shebangs
        actual_commands = [
            line.strip() for line in f 
            if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("!")
        ]

    assert actual_commands == expected_commands, (
        f"The iptables commands in {script_path} are incorrect or not in the right order.\n"
        f"Expected: {expected_commands}\n"
        f"Found: {actual_commands}"
    )