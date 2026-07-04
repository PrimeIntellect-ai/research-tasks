# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) >= 3, f"Audit report must contain at least 3 lines, found {len(lines)}"

    assert lines[0] == "CWE-79", f"Line 1 (XSS CWE) is incorrect: {lines[0]}"
    assert lines[1] in ["CWE-77", "CWE-78"], f"Line 2 (Command Injection CWE) is incorrect: {lines[1]}"
    assert lines[2] in ["666", "0666"], f"Line 3 (Initial permissions) is incorrect: {lines[2]}"

def test_credentials_rotated_and_permissions():
    creds_path = "/home/user/legacy_auth_app/creds.conf"
    assert os.path.isfile(creds_path), f"Credentials file missing at {creds_path}"

    with open(creds_path, "r") as f:
        content = f.read()

    assert "DB_PASS=SuperSecretRotate99!" in content, "Credentials were not rotated correctly in creds.conf"

    st = os.stat(creds_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions on creds.conf are incorrect. Expected 0600, got {oct(perms)}"

def test_compiled_cgi_functionality():
    cgi_path = "/home/user/legacy_auth_app/auth_app.cgi"
    assert os.path.isfile(cgi_path), f"Compiled CGI application not found at {cgi_path}"
    assert os.access(cgi_path, os.X_OK), f"CGI application at {cgi_path} is not executable"

    # Test valid input
    env = os.environ.copy()
    env["QUERY_STRING"] = "username=admin123"
    result_valid = subprocess.run([cgi_path], env=env, capture_output=True, text=True)
    assert "Invalid input" not in result_valid.stdout, "Valid input was incorrectly rejected."

    # Test invalid input (non-alphanumeric)
    env["QUERY_STRING"] = "username=admin;"
    result_invalid = subprocess.run([cgi_path], env=env, capture_output=True, text=True)
    assert result_invalid.returncode == 1, f"Expected exit code 1 for invalid input, got {result_invalid.returncode}"
    assert "<html><body>Invalid input</body></html>" in result_invalid.stdout, "CGI did not print correct invalid input message for non-alphanumeric input."

    # Test empty username
    env["QUERY_STRING"] = "username="
    result_empty = subprocess.run([cgi_path], env=env, capture_output=True, text=True)
    assert result_empty.returncode == 1, f"Expected exit code 1 for empty username, got {result_empty.returncode}"
    assert "<html><body>Invalid input</body></html>" in result_empty.stdout, "CGI did not print correct invalid input message for empty username."

    # Test missing username
    env["QUERY_STRING"] = "otherparam=123"
    result_missing = subprocess.run([cgi_path], env=env, capture_output=True, text=True)
    assert result_missing.returncode == 1, f"Expected exit code 1 for missing username, got {result_missing.returncode}"
    assert "<html><body>Invalid input</body></html>" in result_missing.stdout, "CGI did not print correct invalid input message for missing username."