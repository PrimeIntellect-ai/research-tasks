# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import subprocess

def base64url_decode(input_str):
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def base64url_encode(input_bytes):
    return base64.urlsafe_b64encode(input_bytes).rstrip(b'=')

def test_staging_secret_cracked():
    token_path = "/home/user/staging_token.jwt"
    wordlist_path = "/home/user/wordlist.txt"
    secret_output_path = "/home/user/staging_secret.txt"

    assert os.path.isfile(token_path), f"Missing file: {token_path}"
    assert os.path.isfile(wordlist_path), f"Missing file: {wordlist_path}"
    assert os.path.isfile(secret_output_path), f"Missing file: {secret_output_path}"

    with open(token_path, 'r') as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, "Staging token is not a valid JWT"
    header_payload = f"{parts[0]}.{parts[1]}".encode()
    target_sig = parts[2]

    with open(wordlist_path, 'r') as f:
        words = [line.strip() for line in f if line.strip()]

    # Derive the correct secret from the wordlist
    derived_secret = None
    for word in words:
        sig = hmac.new(word.encode(), header_payload, hashlib.sha256).digest()
        encoded_sig = base64url_encode(sig).decode()
        if encoded_sig == target_sig:
            derived_secret = word
            break

    assert derived_secret is not None, "Could not derive the staging secret from the wordlist and token."

    with open(secret_output_path, 'r') as f:
        student_secret = f.read().strip()

    assert student_secret == derived_secret, f"The cracked secret in {secret_output_path} is incorrect. Expected the derived secret, but got something else."

def test_prod_admin_jwt_structure():
    jwt_path = "/home/user/prod_admin.jwt"
    assert os.path.isfile(jwt_path), f"Missing file: {jwt_path}"

    with open(jwt_path, 'r') as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) >= 2, f"The token in {jwt_path} does not have enough segments to be a JWT."

    header_b64 = parts[0]
    payload_b64 = parts[1]
    sig_b64 = parts[2] if len(parts) == 3 else ""

    try:
        header = json.loads(base64url_decode(header_b64).decode('utf-8'))
        payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))
    except Exception as e:
        assert False, f"Failed to decode and parse header or payload JSON: {e}"

    assert "alg" in header, "Header is missing 'alg' field."
    assert header["alg"].lower() == "none", f"Expected 'alg' to be 'none', got '{header['alg']}'."

    assert "user" in payload, "Payload is missing 'user' field."
    assert payload["user"] == "admin", f"Expected 'user' to be 'admin', got '{payload['user']}'."

    assert sig_b64 == "", "Signature must be empty for 'none' algorithm."

def test_prod_gateway_execution():
    jwt_path = "/home/user/prod_admin.jwt"
    script_path = "/home/user/prod_gateway.sh"

    assert os.path.isfile(jwt_path), f"Missing file: {jwt_path}"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"

    with open(jwt_path, 'r') as f:
        token = f.read().strip()

    result = subprocess.run([script_path, token], capture_output=True, text=True)

    assert result.returncode == 0, f"Script exited with non-zero code {result.returncode}. Stderr: {result.stderr.strip()}"
    output = result.stdout.strip()
    expected_output = "Access Granted: admin"
    assert output == expected_output, f"Script output was '{output}', expected '{expected_output}'."