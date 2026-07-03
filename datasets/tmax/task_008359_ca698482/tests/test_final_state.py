# test_final_state.py

import os
import subprocess
import json
import base64
import pytest

def add_padding(b64_string):
    """Adds missing padding to a base64url encoded string."""
    return b64_string + "=" * (-len(b64_string) % 4)

def test_task1_jwt_forgery():
    script_path = "/home/user/forge_jwt.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"forge_jwt.py failed to execute. Error: {result.stderr}"

    jwt_str = result.stdout.strip()
    parts = jwt_str.split('.')
    assert len(parts) == 3, f"Forged JWT must have exactly 3 parts separated by dots. Got {len(parts)} parts."
    assert parts[2] == "", "The signature part of the forged JWT must be empty."

    try:
        header_bytes = base64.urlsafe_b64decode(add_padding(parts[0]))
        header = json.loads(header_bytes.decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Could not decode or parse JWT header: {e}")

    try:
        payload_bytes = base64.urlsafe_b64decode(add_padding(parts[1]))
        payload = json.loads(payload_bytes.decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Could not decode or parse JWT payload: {e}")

    assert header.get("alg", "").lower() == "none", f"Header 'alg' must be 'none' (case-insensitive). Got: {header.get('alg')}"
    assert header.get("typ") == "JWT", f"Header 'typ' must be 'JWT'. Got: {header.get('typ')}"

    assert payload.get("user") == "admin", f"Payload 'user' must be 'admin'. Got: {payload.get('user')}"
    assert payload.get("role") == "superuser", f"Payload 'role' must be 'superuser'. Got: {payload.get('role')}"

def test_task2_flagged_ips():
    output_path = "/home/user/flagged_ips.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = f.readlines()

    found_ips = set(line.strip() for line in lines if line.strip())
    expected_ips = {"10.0.0.5", "192.168.1.99"}

    assert found_ips == expected_ips, f"The flagged IPs are incorrect. Expected {expected_ips}, but got {found_ips}."
    assert len(lines) == len(found_ips), "The flagged_ips.txt file should contain exactly one IP per line with no duplicates or blank lines."

def test_task3_cert_status():
    status_path = "/home/user/cert_status.txt"
    assert os.path.isfile(status_path), f"Output file {status_path} does not exist."

    with open(status_path, "r") as f:
        content = f.read().strip()

    assert content == "INVALID", f"The certificate status is incorrect. Expected 'INVALID', but got '{content}'."