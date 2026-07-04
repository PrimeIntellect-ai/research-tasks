# test_final_state.py

import os
import subprocess
import pytest

def test_ca_chain_exists_and_valid():
    chain_path = '/home/user/certs/ca-chain.pem'
    assert os.path.isfile(chain_path), f"File {chain_path} is missing."

    with open(chain_path, 'r') as f:
        chain_content = f.read()

    cert_count = chain_content.count('BEGIN CERTIFICATE')
    assert cert_count >= 2, f"ca-chain.pem should contain at least root and intermediate certs, found {cert_count}."

def test_audit_tool_binary():
    tool_path = '/home/user/audit_tool'
    assert os.path.isfile(tool_path), f"audit_tool binary missing at {tool_path}."
    assert os.access(tool_path, os.X_OK), f"audit_tool at {tool_path} is not executable."

    try:
        output = subprocess.check_output(['ldd', tool_path], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ldd on {tool_path}: {e.output.decode()}")

    assert 'libcrypto' in output, "audit_tool is not linked to libcrypto."

def test_audit_trail_log():
    log_path = '/home/user/audit_trail.log'
    assert os.path.isfile(log_path), f"audit_trail.log missing at {log_path}."

    with open(log_path, 'r') as f:
        log_content = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected = [
        "Test 1:",
        "AUDIT: [REJECT] Cert invalid",
        "Test 2:",
        "AUDIT: [REJECT] Insecure algorithm",
        "Test 3:",
        "AUDIT: [REJECT] XSS detected",
        "Test 4:",
        "AUDIT: [PASS] Request accepted"
    ]

    assert len(log_content) == len(expected), f"Expected {len(expected)} lines in log, got {len(log_content)}."

    for i, (actual, exp) in enumerate(zip(log_content, expected)):
        assert actual == exp, f"Line {i+1} mismatch. Expected: '{exp}', Got: '{actual}'"