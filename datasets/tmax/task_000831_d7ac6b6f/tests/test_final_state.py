# test_final_state.py

import os
import json
import re
import subprocess
import pytest

SERVICE_DIR = "/home/user/service"
TOKEN_FILE = os.path.join(SERVICE_DIR, "token.txt")
WRAPPER_SCRIPT = os.path.join(SERVICE_DIR, "wrapper.py")
SERVER_SCRIPT = os.path.join(SERVICE_DIR, "server.py")
REPORT_FILE = "/home/user/security_report.json"

def test_report_json_and_token():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."

    with open(REPORT_FILE, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_FILE} is not valid JSON.")

    assert "env_var_discovered" in report, "Report missing 'env_var_discovered'."
    assert report["env_var_discovered"] == "APP_AUTH_SECRET", "Incorrect environment variable discovered."

    assert "new_token" in report, "Report missing 'new_token'."
    new_token = report["new_token"]
    assert re.match(r"^[a-f0-9]{32}$", new_token), "New token must be a 32-character lowercase hex string."

    assert os.path.isfile(TOKEN_FILE), f"Token file {TOKEN_FILE} does not exist."
    with open(TOKEN_FILE, 'r') as f:
        token_content = f.read().strip()

    assert token_content == new_token, "Content of token.txt does not match 'new_token' in report."

def test_wrapper_fix():
    assert os.path.isfile(WRAPPER_SCRIPT), f"Wrapper script {WRAPPER_SCRIPT} does not exist."

    with open(WRAPPER_SCRIPT, 'r') as f:
        content = f.read()

    assert "OLD_TOKEN_123" not in content, "Wrapper script still contains the old hardcoded token."
    assert "token.txt" in content, "Wrapper script does not seem to read from token.txt."
    assert "APP_AUTH_SECRET" in content, "Wrapper script does not use the APP_AUTH_SECRET environment variable."

    # Run the wrapper script to ensure it works
    result = subprocess.run(['python3', WRAPPER_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"wrapper.py failed to execute correctly. stderr: {result.stderr}"
    assert result.stdout.strip() == "OK", "wrapper.py did not output 'OK'."

def test_server_fix():
    assert os.path.isfile(SERVER_SCRIPT), f"Server script {SERVER_SCRIPT} does not exist."

    with open(SERVER_SCRIPT, 'r') as f:
        content = f.read()

    assert "127.0.0.1" in content, "Server script does not bind to 127.0.0.1."
    assert "0.0.0.0" not in content, "Server script still binds to 0.0.0.0."

    # Check for CSP header
    csp_pattern = re.compile(r"Content-Security-Policy.*default-src\s+'self'", re.IGNORECASE)
    assert csp_pattern.search(content), "Server script does not properly send the Content-Security-Policy header."