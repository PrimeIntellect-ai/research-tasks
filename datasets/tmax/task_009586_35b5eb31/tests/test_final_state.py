# test_final_state.py

import os
import subprocess
import pytest

C_FILE = "/home/user/auth_server.c"
BIN_FILE = "/home/user/auth_server"
RESULT_FILE = "/home/user/auth_result.txt"

def test_source_code_constraints():
    assert os.path.isfile(C_FILE), f"Source file {C_FILE} is missing."
    with open(C_FILE, "r") as f:
        content = f.read()

    assert 'unsetenv("AUTH_TOKEN")' in content.replace(" ", ""), "The source code does not contain unsetenv(\"AUTH_TOKEN\")."
    assert "argv[1]" not in content, "The source code still contains references to argv[1], which should be removed."

def test_executable_exists():
    assert os.path.isfile(BIN_FILE), f"Executable {BIN_FILE} is missing. Did you compile it?"
    assert os.access(BIN_FILE, os.X_OK), f"File {BIN_FILE} is not executable."

def run_auth_server(env_vars=None):
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)

    env = os.environ.copy()
    if env_vars is not None:
        env.update(env_vars)
    else:
        env.pop("AUTH_TOKEN", None)

    subprocess.run([BIN_FILE], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r") as f:
            return f.read().strip()
    return None

def test_valid_token():
    # Base64 for "SuperSecretAppToken2024"
    result = run_auth_server({"AUTH_TOKEN": "U3VwZXJTZWNyZXRBcHBUb2tlbjIwMjQ="})
    assert result == "AUTH_SUCCESS", f"Expected AUTH_SUCCESS for valid token, got {result}"

def test_invalid_token():
    # Base64 for "BadToken"
    result = run_auth_server({"AUTH_TOKEN": "QmFkVG9rZW4="})
    assert result == "AUTH_FAILURE", f"Expected AUTH_FAILURE for invalid token, got {result}"

def test_missing_token():
    result = run_auth_server()
    assert result == "AUTH_FAILURE", f"Expected AUTH_FAILURE for missing token, got {result}"