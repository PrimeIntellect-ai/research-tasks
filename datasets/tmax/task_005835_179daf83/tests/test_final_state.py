# test_final_state.py

import os
import subprocess
import pytest

HOME_DIR = "/home/user"
LOGS_DIR = os.path.join(HOME_DIR, "logs")
AUTH_LOG = os.path.join(LOGS_DIR, "auth.log")
AUTH_CLEAN_LOG = os.path.join(LOGS_DIR, "auth_clean.log")
SUCCESS_TXT = os.path.join(HOME_DIR, "success.txt")
KEYGEN_C = os.path.join(HOME_DIR, "keygen.c")
KEYGEN_BIN = os.path.join(HOME_DIR, "keygen")

SALT = "wX9kP2mR4vLz"

def test_success_txt_exists_and_content():
    assert os.path.isfile(SUCCESS_TXT), f"File not found: {SUCCESS_TXT}"
    with open(SUCCESS_TXT, "r") as f:
        content = f.read().strip()

    expected = "ACCESS GRANTED. FLAG: DEVSEC_POLICY_ENFORCED_99"
    assert content == expected, f"Content of {SUCCESS_TXT} is incorrect. Expected '{expected}', got '{content}'."

def test_auth_clean_log_exists_and_content():
    assert os.path.isfile(AUTH_CLEAN_LOG), f"File not found: {AUTH_CLEAN_LOG}"

    with open(AUTH_CLEAN_LOG, "r") as f:
        content = f.read()

    expected_lines = [
        "[INFO] User admin logged in.",
        "[DEBUG] Token validation failed. Salt used was [REDACTED]",
        "[INFO] User test failed login.",
        "[DEBUG] Initialization complete. Loaded salt: [REDACTED]"
    ]

    for line in expected_lines:
        assert line in content, f"Expected redacted log line '{line}' not found in {AUTH_CLEAN_LOG}."

    assert SALT not in content, f"The secret salt '{SALT}' was found in {AUTH_CLEAN_LOG}, it should be redacted."

def test_keygen_exists_and_functional():
    assert os.path.isfile(KEYGEN_C), f"C source file not found: {KEYGEN_C}"
    assert os.path.isfile(KEYGEN_BIN), f"Compiled binary not found: {KEYGEN_BIN}"
    assert os.access(KEYGEN_BIN, os.X_OK), f"File is not executable: {KEYGEN_BIN}"

    # Test the keygen logic
    test_username = "testuser"
    expected_token = "".join(f"{ord(c) ^ ord(SALT[i % len(SALT)]):02x}" for i, c in enumerate(test_username))

    try:
        result = subprocess.run([KEYGEN_BIN, test_username], capture_output=True, text=True, timeout=2)
        output = result.stdout.strip()
        assert output == expected_token, f"Keygen output incorrect. Expected '{expected_token}', got '{output}'."
    except Exception as e:
        pytest.fail(f"Failed to execute {KEYGEN_BIN}: {e}")