# test_final_state.py
import os
import re
import pytest

def test_cwe_identification():
    """Verify the correct CWE identifier was identified and saved."""
    cwe_path = "/home/user/cwe.txt"
    assert os.path.exists(cwe_path), f"Missing required file: {cwe_path}"

    with open(cwe_path, "r") as f:
        content = f.read().strip()

    assert content == "CWE-125", f"Incorrect CWE identifier in {cwe_path}. Expected 'CWE-125', got '{content}'."

def test_attacker_ip_extraction():
    """Verify the attacker IP was correctly extracted from the log based on the malicious payload."""
    log_path = "/home/user/ids.log"
    assert os.path.exists(log_path), f"Setup error: Missing {log_path}"

    # Derive the expected IP by finding the out-of-bounds read payload (01 03)
    expected_ip = None
    with open(log_path, "r") as f:
        for line in f:
            if "[01 03]" in line:
                # Log format: [Timestamp] [IP Address] [Hex Payload]
                match = re.search(r'\[.*?\] \[(.*?)\] \[01 03\]', line)
                if match:
                    expected_ip = match.group(1)
                    break

    assert expected_ip is not None, "Setup error: Could not find the malicious payload '[01 03]' in ids.log"

    ip_path = "/home/user/attacker_ip.txt"
    assert os.path.exists(ip_path), f"Missing required file: {ip_path}"

    with open(ip_path, "r") as f:
        content = f.read().strip()

    assert content == expected_ip, f"Incorrect attacker IP in {ip_path}. Expected '{expected_ip}', got '{content}'."

def test_evidence_recovery():
    """Verify the evidence flag was successfully recovered and saved."""
    server_path = "/home/user/server.cpp"
    assert os.path.exists(server_path), f"Setup error: Missing {server_path}"

    # Derive the expected flag directly from the source code
    expected_flag = None
    with open(server_path, "r") as f:
        content = f.read()
        match = re.search(r'(FLAG\{[^}]+\})', content)
        if match:
            expected_flag = match.group(1)

    assert expected_flag is not None, "Setup error: Could not find the FLAG pattern in server.cpp"

    evidence_path = "/home/user/evidence.txt"
    assert os.path.exists(evidence_path), f"Missing required file: {evidence_path}"

    with open(evidence_path, "r") as f:
        recovered_flag = f.read().strip()

    assert recovered_flag == expected_flag, f"Incorrect evidence flag in {evidence_path}. Expected '{expected_flag}', got '{recovered_flag}'."