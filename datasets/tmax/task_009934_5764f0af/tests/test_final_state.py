# test_final_state.py

import os
import json
import pytest

def test_recovered_token():
    token_path = "/home/user/recovered_token.txt"
    assert os.path.exists(token_path), f"File {token_path} does not exist. The exploit script must generate it."

    with open(token_path, "r") as f:
        token = f.read().strip()

    expected_token = "FLAG-9a8b7c6d5e4f3g2h1i0j"
    assert token == expected_token, f"Incorrect token recovered. Expected '{expected_token}', but got '{token}'."

def test_security_json_csp():
    security_path = "/home/user/security.json"
    assert os.path.exists(security_path), f"File {security_path} does not exist."

    with open(security_path, "r") as f:
        try:
            sec_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {security_path} does not contain valid JSON.")

    csp_key = "Content-Security-Policy"
    assert csp_key in sec_data, f"Key '{csp_key}' is missing in {security_path}."

    expected_csp = "default-src 'self'"
    actual_csp = sec_data[csp_key]
    assert actual_csp == expected_csp, f"Incorrect CSP configuration. Expected '{expected_csp}', but got '{actual_csp}'."