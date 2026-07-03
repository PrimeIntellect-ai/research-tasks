# test_final_state.py

import os
import hmac
import hashlib

def get_expected_token():
    key = b"supersecret"
    msg = b"admin_access"
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def test_admin_token_file():
    token_path = "/home/user/admin_token.txt"
    assert os.path.exists(token_path), f"File {token_path} is missing."
    assert os.path.isfile(token_path), f"{token_path} should be a file."

    with open(token_path, "r") as f:
        content = f.read().strip()

    expected_token = get_expected_token()
    assert content == expected_token, f"Expected token {expected_token}, but got {content} in {token_path}."

def test_policy_conf_updated():
    policy_path = "/home/user/policy.conf"
    assert os.path.exists(policy_path), f"File {policy_path} is missing."

    with open(policy_path, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 2, f"{policy_path} should have at least 2 lines."

    first_line = lines[0].strip()
    expected_token = get_expected_token()
    expected_first_line = f"ALLOW ADMIN {expected_token}"

    assert first_line == expected_first_line, f"Expected first line of {policy_path} to be '{expected_first_line}', but got '{first_line}'."

    # Check that the rest of the file is unchanged
    assert lines[1].strip() == "ALLOW USER 1234", f"Expected second line of {policy_path} to remain 'ALLOW USER 1234'."