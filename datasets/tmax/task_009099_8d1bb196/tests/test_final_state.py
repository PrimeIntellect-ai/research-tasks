# test_final_state.py

import os
import json
import pytest

def test_flag_content():
    """Verify that flag.txt contains the exact contents of secret.txt."""
    flag_path = "/home/user/flag.txt"
    secret_path = "/home/user/secret.txt"

    assert os.path.isfile(flag_path), f"File not found: {flag_path}"
    assert os.path.isfile(secret_path), f"File not found: {secret_path}"

    with open(secret_path, "r") as f:
        expected_secret = f.read().strip()

    with open(flag_path, "r") as f:
        actual_flag = f.read().strip()

    assert actual_flag == expected_secret, f"Contents of {flag_path} do not match the expected secret."

def test_request_id_validity():
    """Verify that request_id.txt contains a valid request_id for a successful exploit."""
    req_id_path = "/home/user/request_id.txt"
    log_path = "/home/user/app.log"

    assert os.path.isfile(req_id_path), f"File not found: {req_id_path}"
    assert os.path.isfile(log_path), f"File not found: {log_path}"

    with open(req_id_path, "r") as f:
        req_id = f.read().strip()

    assert req_id, f"File {req_id_path} is empty."

    found = False
    with open(log_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if data.get("request_id") == req_id:
                    if data.get("status") == 200 and "/admin/export" in data.get("path", ""):
                        found = True
                        break
            except json.JSONDecodeError:
                continue

    assert found, f"Request ID '{req_id}' not found in {log_path} or did not match a successful exploit request (status 200, path /admin/export)."