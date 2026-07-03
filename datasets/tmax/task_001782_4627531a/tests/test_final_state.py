# test_final_state.py
import json
import os
import pytest

def test_audit_trail_exists_and_valid():
    audit_file = "/home/user/audit_trail.json"
    assert os.path.isfile(audit_file), f"File {audit_file} does not exist. The audit trail was not generated."

    with open(audit_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {audit_file} is not valid JSON.")

    expected_keys = {"salt", "cracked_password", "auth_status_code", "auth_response_body"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Audit trail is missing keys: {missing_keys}"

    assert data["salt"] == "S4lTy_B3v3r4g3!!", f"Incorrect salt extracted: {data['salt']}"
    assert data["cracked_password"] == "bluebird99", f"Incorrect cracked password: {data['cracked_password']}"
    assert data["auth_status_code"] == 200, f"Incorrect auth status code: {data['auth_status_code']}"
    assert data["auth_response_body"] == '{"status":"success","token":"AUTH_TOKEN_9932"}', f"Incorrect auth response body: {data['auth_response_body']}"

def test_cracker_cpp_exists():
    cpp_file = "/home/user/cracker.cpp"
    assert os.path.isfile(cpp_file), f"File {cpp_file} does not exist. The C++ cracker program was not written."