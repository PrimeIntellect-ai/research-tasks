# test_final_state.py
import os
import base64
import json

def test_final_token_correct():
    token_file = "/home/user/final_token.txt"
    assert os.path.exists(token_file), f"File missing: {token_file}"
    assert os.path.isfile(token_file), f"Not a file: {token_file}"

    # Compute expected token based on the rules in the patch
    header = {"alg": "CUSTOM", "typ": "AUTH"}
    payload = {"user": "integration_tester", "role": "admin", "exp": 1735689600}

    h_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')

    data = f"{h_b64}.{p_b64}"

    h = 5381
    for c in data:
        h = ((h << 5) + h) + ord(c)
    checksum = f"{abs(h) % 1000000:06d}"

    expected_token = f"{data}.{checksum}"

    with open(token_file, "r") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_token, f"Token in {token_file} is incorrect. Expected '{expected_token}', got '{actual_token}'"