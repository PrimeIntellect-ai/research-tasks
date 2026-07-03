# test_final_state.py

import os
import json
import subprocess
import base64
import pytest

def get_expected_subject():
    """Extracts the JWT from the ELF binary and decodes the subject claim."""
    binary_path = "/home/user/target_binary.elf"
    token_path = "/tmp/extracted_auth_token.txt"

    try:
        subprocess.run(
            ["objcopy", "-O", "binary", "--only-section=.auth_token", binary_path, token_path],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract .auth_token section: {e.stderr.decode()}")

    with open(token_path, "r") as f:
        token = f.read().strip()

    # A JWT has 3 parts separated by dots: header.payload.signature
    parts = token.split(".")
    if len(parts) != 3:
        pytest.fail("Extracted token is not a valid JWT format.")

    payload_b64 = parts[1]
    # Add base64 padding if necessary
    payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)

    try:
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes)
    except Exception as e:
        pytest.fail(f"Failed to decode JWT payload: {e}")

    return payload.get("sub")

def test_result_json_exists():
    """Verify that the result.json file was created."""
    result_path = "/home/user/result.json"
    assert os.path.exists(result_path), f"The output file {result_path} is missing."
    assert os.path.isfile(result_path), f"{result_path} is not a regular file."

def test_result_json_content():
    """Verify that result.json contains the correct verification results."""
    result_path = "/home/user/result.json"

    if not os.path.exists(result_path):
        pytest.fail(f"{result_path} does not exist, cannot check content.")

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} does not contain valid JSON.")

    expected_sub = get_expected_subject()

    assert data.get("elf_valid") is True, "elf_valid is not true. The binary should be considered valid."
    assert data.get("chain_valid") is True, "chain_valid is not true. The certificate chain should be valid."
    assert data.get("jwt_valid") is True, "jwt_valid is not true. The JWT signature should be valid."
    assert data.get("jwt_subject") == expected_sub, f"jwt_subject is incorrect. Expected '{expected_sub}', got '{data.get('jwt_subject')}'."