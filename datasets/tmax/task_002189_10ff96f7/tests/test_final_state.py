# test_final_state.py

import os
import subprocess
import json
import base64
import pytest

def decode_b64url(s):
    s = s.replace('-', '+').replace('_', '/')
    return base64.b64decode(s + '=' * (-len(s) % 4))

def test_forge_token_script_exists():
    script_path = '/home/user/forge_token.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_forge_token_output():
    script_path = '/home/user/forge_token.sh'

    try:
        result = subprocess.run(['bash', script_path], capture_output=True, text=True, check=True)
        token = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing {script_path} failed: {e.stderr}")

    parts = token.split('.')
    assert len(parts) == 3, "The output of the script is not a valid 3-part JWT."
    assert parts[2] == '', "The signature part of the token must be empty for 'none' algorithm."

    try:
        header = json.loads(decode_b64url(parts[0]))
        payload = json.loads(decode_b64url(parts[1]))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT header/payload: {e}")

    assert header.get('alg', '').lower() == 'none', "The JWT header 'alg' must be 'none'."
    assert payload.get('aud') == 'corp.auth.internal', "The JWT payload 'aud' must match the certificate CN."
    assert payload.get('role') == 'superuser', "The JWT payload 'role' must be 'superuser'."

def test_audit_result_flag():
    result_path = '/home/user/audit_result.txt'
    assert os.path.isfile(result_path), f"{result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{jwt_alg_none_privesc_7739}"
    assert content == expected_flag, f"The file {result_path} does not contain the correct flag."