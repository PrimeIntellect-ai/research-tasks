# test_final_state.py
import os
import subprocess
import base64
import pytest

def test_cwe_identification():
    """Verify that the student correctly identified the CWE."""
    cwe_path = "/home/user/cwe.txt"
    assert os.path.exists(cwe_path), f"Required file {cwe_path} is missing. You must write the CWE identifier to this file."

    with open(cwe_path, "r") as f:
        content = f.read().upper()

    assert "CWE-798" in content or "CWE-327" in content, (
        f"The file {cwe_path} does not contain the correct CWE identifier. "
        "Expected CWE-798 (Use of Hard-coded Credentials) or CWE-327."
    )

def test_payload_format():
    """Verify that the payload file exists and contains valid base64."""
    payload_path = "/home/user/payload.txt"
    assert os.path.exists(payload_path), f"Required file {payload_path} is missing."

    with open(payload_path, "r") as f:
        content = f.read().strip()

    assert len(content) > 0, f"The file {payload_path} is empty."

    try:
        base64.b64decode(content, validate=True)
    except Exception as e:
        pytest.fail(f"The content of {payload_path} is not valid base64: {e}")

def test_authentication_bypass():
    """Verify that the crafted payload successfully bypasses the authentication script."""
    script_path = "/home/user/auth_verifier.py"
    payload_path = "/home/user/payload.txt"
    success_log_path = "/home/user/success.log"

    assert os.path.exists(script_path), f"Target script {script_path} is missing."
    assert os.path.exists(payload_path), f"Payload file {payload_path} is missing."

    # Ensure a clean state for the success log
    if os.path.exists(success_log_path):
        os.remove(success_log_path)

    # Execute the verifier script with the payload
    result = subprocess.run(
        ["python3", script_path, payload_path],
        capture_output=True,
        text=True
    )

    assert os.path.exists(success_log_path), (
        f"Authentication bypass failed. The file {success_log_path} was not created.\n"
        f"Script stdout: {result.stdout.strip()}\n"
        f"Script stderr: {result.stderr.strip()}"
    )

    with open(success_log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == "Bypassed", (
        f"Authentication bypass failed. Expected '{success_log_path}' to contain 'Bypassed', "
        f"but found '{log_content}'."
    )