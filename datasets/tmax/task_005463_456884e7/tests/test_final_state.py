# test_final_state.py
import sys
import os
import json
import base64
import hmac
import hashlib
import pytest

def create_valid_token(payload, secret):
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    msg = f"{encoded_header}.{encoded_payload}"
    sig = base64.urlsafe_b64encode(hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()).decode().rstrip('=')
    return f"{msg}.{sig}"

def create_malicious_token(payload):
    header = {"alg": "none", "typ": "JWT"}
    encoded_header = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    return f"{encoded_header}.{encoded_payload}."

def test_token_validation_accuracy():
    # Insert vendored path to ensure we test the patched library
    if '/app/pyjwt-vendored' not in sys.path:
        sys.path.insert(0, '/app/pyjwt-vendored')

    try:
        import jwt
    except ImportError:
        pytest.fail("Failed to import jwt from /app/pyjwt-vendored")

    secret = "supersecret_test_key"
    correct_valid = 0
    correct_malicious = 0
    total_valid = 500
    total_malicious = 500

    # Test valid tokens
    for i in range(total_valid):
        token = create_valid_token({"user": f"user{i}"}, secret)
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            if decoded.get("user") == f"user{i}":
                correct_valid += 1
        except Exception:
            pass

    # Test malicious tokens (alg: none backdoor)
    for i in range(total_malicious):
        token = create_malicious_token({"user": "attacker", "role": "admin"})
        try:
            jwt.decode(token, secret, algorithms=["HS256"])
            # If it decodes successfully, the backdoor is still present
        except Exception:
            # Expected to raise an exception (e.g., InvalidAlgorithmError or DecodeError)
            correct_malicious += 1

    total_tokens = total_valid + total_malicious
    accuracy = (correct_valid + correct_malicious) / total_tokens

    assert accuracy >= 1.0, f"Token Validation Accuracy is {accuracy} ({correct_valid + correct_malicious}/{total_tokens}), expected >= 1.0"

def test_scanner_output():
    ports_file = "/home/user/vulnerable_ports.txt"
    assert os.path.exists(ports_file), f"Expected scanner output file {ports_file} is missing"

    with open(ports_file, "r") as f:
        lines = f.read().splitlines()

    ports = set(line.strip() for line in lines if line.strip())
    expected_ports = {"8004", "8007"}

    assert ports == expected_ports, f"Scanner logged incorrect vulnerable ports. Found: {ports}, Expected: {expected_ports}"

def test_scanner_script_exists():
    scanner_script = "/home/user/scanner.py"
    assert os.path.exists(scanner_script), f"Scanner script {scanner_script} is missing"