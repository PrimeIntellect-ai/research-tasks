# test_final_state.py

import os
import base64
import hmac
import hashlib
import json
import subprocess

def test_jwt_token():
    token_path = '/home/user/payload.token'
    assert os.path.exists(token_path), f"Fail: {token_path} not found"

    with open(token_path, 'r') as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, "Fail: JWT must consist of 3 parts separated by dots"
    header, payload, signature = parts

    secret = "SuperSecretRedTeamK3y!"
    message = f"{header}.{payload}".encode('utf-8')

    # Verify HMAC SHA-256 signature
    expected_sig = hmac.new(secret.encode('utf-8'), message, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).rstrip(b'=').decode('utf-8')

    assert signature == expected_sig_b64, "Fail: JWT signature is invalid. Did you use the correct secret?"

    # Verify payload
    payload_pad = payload + '=' * (-len(payload) % 4)
    try:
        payload_json = json.loads(base64.urlsafe_b64decode(payload_pad).decode('utf-8'))
    except Exception as e:
        assert False, f"Fail: Could not decode JWT payload: {e}"

    expected_payload = {"role": "admin", "cmd": "evade"}
    assert payload_json == expected_payload, f"Fail: JWT payload incorrect. Expected {expected_payload}, got {payload_json}"

def test_tls_certificate_and_key():
    crt_path = '/home/user/c2.crt'
    key_path = '/home/user/c2.key'

    assert os.path.exists(crt_path), f"Fail: {crt_path} not found"
    assert os.path.exists(key_path), f"Fail: {key_path} not found"

    # Check Subject CN
    try:
        subject = subprocess.check_output(['openssl', 'x509', '-in', crt_path, '-noout', '-subject'], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError:
        assert False, "Fail: Invalid certificate format"

    assert "CN = c2.evil-corp.local" in subject or "CN=c2.evil-corp.local" in subject, f"Fail: Certificate CN is incorrect. Subject: {subject.strip()}"

    # Check Modulus Match
    try:
        cert_mod = subprocess.check_output(['openssl', 'x509', '-noout', '-modulus', '-in', crt_path], stderr=subprocess.STDOUT)
        key_mod = subprocess.check_output(['openssl', 'rsa', '-noout', '-modulus', '-in', key_path], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        assert False, "Fail: Error reading private key or certificate"

    assert cert_mod == key_mod, "Fail: Certificate and private key do not match"

    # Check Key Size
    try:
        text_output = subprocess.check_output(['openssl', 'rsa', '-in', key_path, '-text', '-noout'], stderr=subprocess.STDOUT).decode('utf-8')
        assert "Private-Key: (2048 bit" in text_output, "Fail: RSA key size is not 2048 bits"
    except subprocess.CalledProcessError:
        assert False, "Fail: Error reading private key details"