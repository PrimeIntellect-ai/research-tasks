# test_final_state.py

import os
import subprocess
import pytest

def test_server_key_encrypted_with_correct_passphrase():
    key_path = "/home/user/certs/server.key"
    assert os.path.isfile(key_path), f"Private key not found at {key_path}"

    # Check if it's encrypted with AUTH_MASTER_8472
    result = subprocess.run(
        ["openssl", "rsa", "-in", key_path, "-passin", "pass:AUTH_MASTER_8472", "-check", "-noout"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to verify private key with the expected passphrase. OpenSSL output: {result.stderr}"

def test_server_crt_common_name():
    crt_path = "/home/user/certs/server.crt"
    assert os.path.isfile(crt_path), f"Certificate not found at {crt_path}"

    # Check if Common Name is secure-api.internal
    result = subprocess.run(
        ["openssl", "x509", "-in", crt_path, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to read certificate. OpenSSL output: {result.stderr}"
    assert "secure-api.internal" in result.stdout, f"Expected Common Name 'secure-api.internal' not found in certificate subject: {result.stdout}"

def test_auth_validator_accuracy():
    validator_path = "/home/user/auth_validator"
    crt_path = "/home/user/certs/server.crt"
    logs_path = "/app/hidden_test_logs.csv"

    assert os.path.isfile(validator_path), f"auth_validator executable not found at {validator_path}"
    assert os.access(validator_path, os.X_OK), f"auth_validator at {validator_path} is not executable"

    try:
        result = subprocess.run(
            [validator_path, crt_path, logs_path],
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("auth_validator execution timed out.")

    assert result.returncode == 0, f"auth_validator exited with non-zero code {result.returncode}. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]

    expected = [
        "Req1: PASS",
        "Req2: FAIL",
        "Req3: FAIL",
        "Req4: PASS"
    ]

    correct = sum(1 for o, e in zip(output_lines, expected) if o == e)
    accuracy = correct / len(expected) if expected else 0.0

    assert accuracy >= 1.0, f"auth_validator accuracy is {accuracy}, expected >= 1.0. Output was: {output_lines}"