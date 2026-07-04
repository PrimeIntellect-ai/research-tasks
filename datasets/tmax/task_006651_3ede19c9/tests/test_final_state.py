# test_final_state.py

import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"

def test_libauth_so_exists():
    so_path = os.path.join(WORKSPACE_DIR, "lib", "libauth.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist. Did you compile libauth.c correctly?"

def test_auth_db_exists():
    db_path = os.path.join(WORKSPACE_DIR, "auth.db")
    assert os.path.isfile(db_path), f"Database {db_path} does not exist. Did you run migrate.py?"

def test_result_log_contents():
    log_path = os.path.join(WORKSPACE_DIR, "result.log")
    assert os.path.isfile(log_path), f"Result log {log_path} does not exist. Did you make the GET request and save the output?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {log_path} is empty."

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {log_path} does not contain valid JSON. Content: {content}")

    assert "token" in data, f"JSON in {log_path} is missing the 'token' key. Content: {data}"

    expected_token = (42 * 1337) ^ 0xDEAD
    assert data["token"] == expected_token, f"Expected token {expected_token}, but got {data['token']}."