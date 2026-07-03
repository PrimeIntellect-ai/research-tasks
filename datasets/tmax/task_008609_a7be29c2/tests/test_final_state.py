# test_final_state.py

import os
import json
import subprocess
import pytest

def test_secrets_report_exists_and_format():
    report_path = "/home/user/secrets_report.json"
    assert os.path.exists(report_path), f"Verification failed: {report_path} not found."

    with open(report_path, 'r') as r:
        try:
            data = json.load(r)
        except Exception as e:
            pytest.fail(f"Verification failed: Invalid JSON. {e}")

    assert isinstance(data, list), "Verification failed: JSON root must be a list."
    assert len(data) == 2, f"Verification failed: Expected 2 entries, found {len(data)}"

    assert "file" in data[0] and "encrypted_secret" in data[0], "Verification failed: Missing required keys in first entry."
    assert "file" in data[1] and "encrypted_secret" in data[1], "Verification failed: Missing required keys in second entry."

    assert data[0]['file'] == 'app1.conf', f"Verification failed: Expected first file to be 'app1.conf', got '{data[0]['file']}'."
    assert data[1]['file'] == 'app3.conf', f"Verification failed: Expected second file to be 'app3.conf', got '{data[1]['file']}'."

def test_secrets_decryption():
    report_path = "/home/user/secrets_report.json"
    key_path = "/home/user/fernet.key"

    assert os.path.exists(report_path), f"Verification failed: {report_path} not found."
    assert os.path.exists(key_path), f"Verification failed: {key_path} not found."

    with open(report_path, 'r') as r:
        data = json.load(r)

    secret1_enc = data[0]['encrypted_secret']
    secret3_enc = data[1]['encrypted_secret']

    # Use subprocess to perform decryption to strictly avoid third-party imports in the test file
    script = f"""
import sys
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("cryptography library not found")
    sys.exit(3)

key_path = "{key_path}"
with open(key_path, 'rb') as f:
    key = f.read().strip()

try:
    fernet = Fernet(key)
except Exception as e:
    print(f"Invalid Fernet key: {{e}}")
    sys.exit(4)

try:
    secret1 = fernet.decrypt("{secret1_enc}".encode('utf-8')).decode('utf-8')
    secret3 = fernet.decrypt("{secret3_enc}".encode('utf-8')).decode('utf-8')
except Exception as e:
    print(f"Decryption error: {{e}}")
    sys.exit(2)

if secret1 == "admin:supersecret123" and secret3 == "root:toor":
    sys.exit(0)
else:
    print(f"Decrypted secrets do not match. Got: {{secret1}} and {{secret3}}")
    sys.exit(1)
"""

    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True)

    assert result.returncode == 0, f"Verification failed: {result.stdout.strip() or result.stderr.strip() or 'Decryption check failed.'}"