# test_final_state.py

import os
import json
import subprocess
import pytest

def get_expected_compromised_sessions():
    """Derive the expected compromised sessions from the log file and certificates."""
    log_path = "/home/user/gateway_logs.json"
    ca_chain_path = "/home/user/ca-chain.pem"
    certs_dir = "/home/user/certs"

    assert os.path.exists(log_path), f"Gateway logs file missing: {log_path}"

    with open(log_path, 'r') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Gateway logs file does not contain valid JSON: {log_path}")

    compromised_ids = []

    for entry in logs:
        req_id = entry.get("req_id")
        client_cert_file = entry.get("client_cert_file")
        payload = entry.get("payload", "")
        response_code = entry.get("response_code")

        # Condition 3: Successful Authentication
        if response_code != 200:
            continue

        # Condition 2: Malicious Payload
        if "<script>" not in payload and "' OR " not in payload:
            continue

        # Condition 1: Valid Certificate
        cert_path = os.path.join(certs_dir, client_cert_file)
        if not os.path.exists(cert_path):
            continue

        verify_cmd = [
            "openssl", "verify",
            "-CAfile", ca_chain_path,
            cert_path
        ]

        result = subprocess.run(verify_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            compromised_ids.append(req_id)

    return sorted(compromised_ids)

def test_compromised_sessions_file_exists():
    """Test that the compromised_sessions.txt file was created."""
    output_path = "/home/user/compromised_sessions.txt"
    assert os.path.exists(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(output_path), f"Path exists but is not a file: {output_path}"

def test_compromised_sessions_content():
    """Test that the compromised_sessions.txt contains the correct req_ids."""
    output_path = "/home/user/compromised_sessions.txt"
    assert os.path.exists(output_path), f"Output file missing: {output_path}"

    expected_ids = get_expected_compromised_sessions()

    with open(output_path, 'r') as f:
        lines = f.read().splitlines()

    actual_ids = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            try:
                actual_ids.append(int(stripped))
            except ValueError:
                pytest.fail(f"Output file contains non-integer value: '{stripped}'")

    assert actual_ids == expected_ids, (
        f"Output file contents do not match expected compromised req_ids.\n"
        f"Expected: {expected_ids}\n"
        f"Actual:   {actual_ids}"
    )