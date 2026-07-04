# test_final_state.py

import os
import json
import stat
import base64
import subprocess
import pytest

def test_attacker_ip_extracted():
    """Verify that the attacker's IP was correctly identified and saved."""
    ip_file = "/home/user/incident_report/attacker_ip.txt"
    assert os.path.isfile(ip_file), f"File not found: {ip_file}"

    with open(ip_file, "r") as f:
        content = f.read().strip()

    assert content == "10.13.37.99", f"Expected attacker IP '10.13.37.99', but got '{content}'"

def test_blocklist_updated():
    """Verify that the attacker's IP was appended to the blocklist.json."""
    blocklist_path = "/home/user/app/config/blocklist.json"
    assert os.path.isfile(blocklist_path), f"File not found: {blocklist_path}"

    with open(blocklist_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Blocklist file {blocklist_path} is not valid JSON.")

    assert isinstance(data, list), "Blocklist must be a JSON array."
    assert "198.51.100.23" in data, "Original IP '198.51.100.23' is missing from the blocklist."
    assert "10.13.37.99" in data, "Attacker IP '10.13.37.99' was not added to the blocklist."

def test_auth_py_remediated():
    """Verify that auth.py no longer accepts 'alg=none' JWTs."""
    auth_py_path = "/home/user/app/auth.py"
    assert os.path.isfile(auth_py_path), f"File not found: {auth_py_path}"

    # We use a subprocess to execute the check, ensuring we test the module in its environment
    test_script = """
import sys
sys.path.append('/home/user/app')
import auth

token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYmFkZ3V5Iiwicm9sZSI6ImFkbWluIn0."
try:
    auth.decode_token(token, "secret")
    print("VULNERABLE")
    sys.exit(1)
except Exception:
    print("SECURE")
    sys.exit(0)
"""
    result = subprocess.run(["python3", "-c", test_script], capture_output=True, text=True)
    assert result.returncode == 0, "auth.py still successfully decodes tokens with alg=none, vulnerability not remediated."
    assert "SECURE" in result.stdout, "auth.py did not reject the malicious token."

def test_new_secret_generated():
    """Verify the new secret is generated, correctly formatted, and has proper permissions."""
    secret_path = "/home/user/app/config/new_secret.key"
    assert os.path.isfile(secret_path), f"File not found: {secret_path}"

    # Check permissions
    st = os.stat(secret_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Expected file permissions to be 400, but got {oct(perms)}"

    # Check content is base64 and decodes to 32 bytes
    with open(secret_path, "r") as f:
        content = f.read().strip()

    try:
        decoded = base64.b64decode(content, validate=True)
    except Exception:
        pytest.fail(f"Content of {secret_path} is not valid base64.")

    assert len(decoded) == 32, f"Expected decoded secret to be exactly 32 bytes, but got {len(decoded)} bytes."

def test_compromised_key_identified():
    """Verify that the compromised key was correctly identified."""
    report_path = "/home/user/incident_report/compromised_key.txt"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "key_v2.pem", f"Expected compromised key to be 'key_v2.pem', but got '{content}'"