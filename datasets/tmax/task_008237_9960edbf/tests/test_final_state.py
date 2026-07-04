# test_final_state.py
import os
import json
import base64

def test_admin_token_correct():
    token_path = "/home/user/admin_token.txt"
    assert os.path.isfile(token_path), f"File {token_path} is missing."

    with open(token_path, 'r') as f:
        token = f.read().strip()

    # Compute the expected token dynamically
    user_id = "admin_root"
    key = 42
    encrypted = bytearray()
    for char in user_id:
        encrypted.append(ord(char) ^ key)
    expected_token = base64.b64encode(encrypted).decode('utf-8')

    assert token == expected_token, f"The token in {token_path} is incorrect. Expected {expected_token}, got {token}."

def test_safe_csp_correct():
    csp_path = "/home/user/safe_csp.json"
    assert os.path.isfile(csp_path), f"File {csp_path} is missing."

    try:
        with open(csp_path, 'r') as f:
            safe_csp = json.load(f)
    except json.JSONDecodeError:
        assert False, f"File {csp_path} does not contain valid JSON."

    assert isinstance(safe_csp, list), f"The JSON in {csp_path} should be a list of objects."

    # Verify the contents
    ids = sorted([item.get('id') for item in safe_csp if 'id' in item])
    expected_ids = ['app2', 'app4']

    assert ids == expected_ids, f"The filtered CSP rules are incorrect. Expected IDs {expected_ids}, got {ids}."

    # Verify that none of the policies contain 'unsafe-inline' or 'unsafe-eval'
    for item in safe_csp:
        policy = item.get('policy', '')
        assert 'unsafe-inline' not in policy, f"Found 'unsafe-inline' in policy for id {item.get('id')}"
        assert 'unsafe-eval' not in policy, f"Found 'unsafe-eval' in policy for id {item.get('id')}"