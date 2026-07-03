# test_final_state.py

import os
import subprocess
import pytest

def get_expected_fingerprint():
    """Helper to derive the expected SHA-1 fingerprint from the server.pem file."""
    pem_path = "/home/user/server.pem"
    assert os.path.exists(pem_path), f"Missing required file: {pem_path}"

    result = subprocess.run(
        ['openssl', 'x509', '-noout', '-fingerprint', '-sha1', '-in', pem_path],
        capture_output=True, text=True, check=True
    )
    # Output format is expected to be "SHA1 Fingerprint=AA:BB:CC..."
    return result.stdout.strip().split('=')[1]

def test_findings_log_contents():
    log_path = "/home/user/findings.log"
    assert os.path.exists(log_path), f"Missing file: {log_path}"

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 2, f"findings.log must contain exactly 2 lines, but found {len(lines)} lines."

    # Line 1: Firewall port analysis
    expected_port = "9443"
    assert lines[0].strip() == expected_port, f"Line 1 of findings.log is incorrect. Expected '{expected_port}', got '{lines[0]}'."

    # Line 2: SHA-1 Fingerprint
    expected_fp = get_expected_fingerprint()
    assert lines[1].strip() == expected_fp, f"Line 2 of findings.log is incorrect. Expected '{expected_fp}', got '{lines[1]}'."

def test_exploit_py_execution_and_output():
    script_path = "/home/user/exploit.py"
    assert os.path.exists(script_path), f"Missing file: {script_path}"

    # Run the student's exploit script
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"exploit.py failed to execute successfully. Stderr: {result.stderr}"

    output = result.stdout.strip()

    # Derive the expected token based on the logic in crypto_auth.py
    key = b"sUp3r_s3cr3t_k3y"
    msg = b"admin_root_system"
    expected_token = bytes([m ^ key[i % len(key)] for i, m in enumerate(msg)]).hex()

    assert output == expected_token, f"Output of exploit.py is incorrect. Expected '{expected_token}', got '{output}'."