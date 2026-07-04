# test_final_state.py

import os
import re
import subprocess
import pytest

AUTH_TOKEN_PATH = "/home/user/auth.token"
AUTH_SERVICE_BIN = "/home/user/auth_service"
AUTH_SERVICE_SRC = "/home/user/auth_service.cpp"
SERVICE_LOG_PATH = "/home/user/service.log"
REPORT_PATH = "/home/user/report.txt"
OLD_TOKEN = "OLD_TOKEN_XYZ_89324"

def test_auth_token():
    assert os.path.exists(AUTH_TOKEN_PATH), f"File {AUTH_TOKEN_PATH} does not exist."
    assert os.path.isfile(AUTH_TOKEN_PATH), f"{AUTH_TOKEN_PATH} is not a file."

    with open(AUTH_TOKEN_PATH, "r") as f:
        token = f.read().strip()

    assert re.match(r"^[0-9a-f]{32}$", token), f"Token in {AUTH_TOKEN_PATH} is not a 32-character lowercase hex string."

def test_service_log_redaction():
    assert os.path.exists(SERVICE_LOG_PATH), f"File {SERVICE_LOG_PATH} does not exist."

    with open(SERVICE_LOG_PATH, "r") as f:
        content = f.read()

    assert OLD_TOKEN not in content, f"Old token '{OLD_TOKEN}' was not completely redacted from {SERVICE_LOG_PATH}."

    redacted_count = content.count("[REDACTED]")
    assert redacted_count == 2, f"Expected exactly 2 instances of '[REDACTED]' in {SERVICE_LOG_PATH}, found {redacted_count}."

def test_auth_service_execution():
    assert os.path.exists(AUTH_SERVICE_BIN), f"Executable {AUTH_SERVICE_BIN} does not exist."
    assert os.access(AUTH_SERVICE_BIN, os.X_OK), f"File {AUTH_SERVICE_BIN} is not executable."

    with open(AUTH_TOKEN_PATH, "r") as f:
        valid_token = f.read().strip()

    # Test with valid token
    result_valid = subprocess.run([AUTH_SERVICE_BIN, valid_token], capture_output=True, text=True)
    assert result_valid.stdout.strip() == "Access Granted", "Executable did not grant access with the correct token."

    # Test with invalid token
    result_invalid = subprocess.run([AUTH_SERVICE_BIN, "invalid_token_1234567890123456789"], capture_output=True, text=True)
    assert result_invalid.stdout.strip() == "Access Denied", "Executable did not deny access with an incorrect token."

def test_source_code_fixed():
    assert os.path.exists(AUTH_SERVICE_SRC), f"Source code {AUTH_SERVICE_SRC} does not exist."

    with open(AUTH_SERVICE_SRC, "r") as f:
        content = f.read()

    assert OLD_TOKEN not in content, f"The hardcoded token '{OLD_TOKEN}' is still present in {AUTH_SERVICE_SRC}."

def test_report_content():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) >= 2, f"Report file {REPORT_PATH} does not have at least 2 lines."

    cwe_line = lines[0]
    assert cwe_line in ["CWE-798", "CWE-259"], f"First line of report must be CWE-798 or CWE-259, got '{cwe_line}'."

    with open(AUTH_TOKEN_PATH, "r") as f:
        valid_token = f.read().strip()

    token_line = lines[1]
    assert token_line == valid_token, f"Second line of report must be the new token '{valid_token}', got '{token_line}'."