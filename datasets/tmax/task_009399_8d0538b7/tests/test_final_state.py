# test_final_state.py

import os
import subprocess
import pytest

def test_leaked_token():
    token_file = "/home/user/leaked_token.txt"
    assert os.path.exists(token_file), f"File {token_file} does not exist."
    with open(token_file, "r") as f:
        content = f.read().strip()
    assert content == "x9f8c7b6a5d4e3f2g1h0", f"Leaked token is incorrect. Expected 'x9f8c7b6a5d4e3f2g1h0', got '{content}'."

def test_binary_exists():
    binary_path = "/home/user/auth_service_fixed"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_binary_no_cookie():
    binary_path = "/home/user/auth_service_fixed"
    env = os.environ.copy()
    if "AUTH_COOKIE" in env:
        del env["AUTH_COOKIE"]

    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)
    assert result.returncode == 1, f"Expected exit code 1 when no cookie is provided, got {result.returncode}."
    assert "Error: No cookie" in result.stdout, f"Expected 'Error: No cookie' in stdout, got '{result.stdout}'."

def test_binary_correct_cookie():
    binary_path = "/home/user/auth_service_fixed"
    env = os.environ.copy()
    env["AUTH_COOKIE"] = "Cookie: session=x9f8c7b6a5d4e3f2g1h0"

    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Expected exit code 0 with correct cookie, got {result.returncode}."
    assert "Authentication successful." in result.stdout, f"Expected 'Authentication successful.' in stdout, got '{result.stdout}'."

def test_binary_incorrect_cookie():
    binary_path = "/home/user/auth_service_fixed"
    env = os.environ.copy()
    env["AUTH_COOKIE"] = "Cookie: session=wrong_token_here"

    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)
    assert result.returncode == 1, f"Expected exit code 1 with incorrect cookie, got {result.returncode}."
    assert "Authentication failed." in result.stdout, f"Expected 'Authentication failed.' in stdout, got '{result.stdout}'."