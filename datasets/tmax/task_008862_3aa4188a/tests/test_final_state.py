# test_final_state.py

import os
import json
import base64
import hashlib
import pytest

def get_expected_token():
    log_path = "/home/user/access.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    target_cookie = None
    with open(log_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "X-Action: Rotate-Target" in line:
            # Find the cookie line in this block
            for j in range(i, len(lines)):
                if lines[j].startswith("Cookie: auth_session="):
                    target_cookie = lines[j].strip().split("Cookie: auth_session=")[1]
                    break
            break

    assert target_cookie is not None, "Could not find target cookie in access.log"

    decoded_json = base64.b64decode(target_cookie).decode('utf-8')
    data = json.loads(decoded_json)

    old_secret = data['secret']
    user = data['user']

    new_secret_raw = old_secret + "ROTATED"
    new_secret_hash = hashlib.sha256(new_secret_raw.encode('utf-8')).hexdigest()

    new_data = {"user": user, "secret": new_secret_hash}
    new_json_str = json.dumps(new_data, separators=(',', ':'))

    expected_token = base64.b64encode(new_json_str.encode('utf-8')).decode('utf-8')
    return expected_token

def test_rotate_script_exists():
    script_path = "/home/user/rotate.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_new_token_correct():
    token_path = "/home/user/new_token.txt"
    assert os.path.isfile(token_path), f"The token file {token_path} was not created."

    with open(token_path, 'r') as f:
        actual_token = f.read().strip()

    expected_token = get_expected_token()

    assert actual_token == expected_token, (
        f"The token in {token_path} is incorrect. "
        f"Expected '{expected_token}', but got '{actual_token}'."
    )