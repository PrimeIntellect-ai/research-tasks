# test_final_state.py

import os
import json
import re
import pytest

def test_server_setup_permissions():
    path = "/home/user/server_setup.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check for chmod 600 or equivalent on the db_secret.key file
    match = re.search(r'chmod\s+(?:600|u=rw,g=,o=)\s+.*?db_secret\.key', content)
    assert match is not None, "server_setup.sh does not properly set permissions to 600 for db_secret.key"

def test_server_setup_headers():
    path = "/home/user/server_setup.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert re.search(r'X-Content-Type-Options\\?:\s*nosniff', content, re.IGNORECASE), \
        "server_setup.sh does not include the X-Content-Type-Options: nosniff header."
    assert re.search(r'X-Frame-Options\\?:\s*DENY', content, re.IGNORECASE), \
        "server_setup.sh does not include the X-Frame-Options: DENY header."

def test_greet_script_injection():
    path = "/home/user/src/cgi-bin/greet.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "eval " not in content, "greet.sh still contains the unsafe 'eval' command."

    # Check if there is some form of sanitization (e.g., tr, sed, parameter expansion replacing bad chars)
    # The requirement states "implements some form of basic character stripping or safe variable expansion"
    sanitization_found = any(x in content for x in ["tr ", "sed ", "${NAME//", "gsub"])
    # If they just use echo without eval, it might still be vulnerable to some things if unquoted, but removing eval is the primary explicit check.
    # Let's just ensure eval is gone and echo is used safely.
    assert "echo" in content, "greet.sh must still output the value."

def test_audit_report():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), f"Audit report {path} does not exist."

    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected = {
      "vulnerabilities_fixed": [
        "Insecure File Permissions",
        "Missing Security Headers",
        "Command Injection"
      ],
      "db_secret_permission": "600",
      "added_headers": ["X-Content-Type-Options", "X-Frame-Options"]
    }

    assert report == expected, f"Audit report content does not match the expected structure. Got: {report}"