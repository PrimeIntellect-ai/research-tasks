# test_final_state.py

import os
import stat
import pytest
import hashlib

def test_compromised_files_logged():
    log_path = "/home/user/compromised_files.txt"
    assert os.path.isfile(log_path), f"Expected log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_compromised = "/home/user/app_env/bin/deploy.sh"
    assert expected_compromised in lines, f"{expected_compromised} was not found in {log_path}."

def test_permission_violations_logged_and_fixed():
    log_path = "/home/user/permission_violations.txt"
    assert os.path.isfile(log_path), f"Expected log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_violations = [
        "/home/user/app_env/bin/suid_tool",
        "/home/user/app_env/config/settings.json"
    ]

    for v in expected_violations:
        assert v in lines, f"Expected violation {v} not found in {log_path}."

        # Check that permissions were actually fixed
        assert os.path.exists(v), f"File {v} is missing."
        st = os.stat(v)

        # Check SUID
        assert not (st.st_mode & stat.S_ISUID), f"SUID bit is still set on {v}."
        # Check SGID
        assert not (st.st_mode & stat.S_ISGID), f"SGID bit is still set on {v}."
        # Check world-writable
        assert not (st.st_mode & stat.S_IWOTH), f"World-writable bit is still set on {v}."

def test_sensitive_data_redacted():
    access_log = "/home/user/app_env/logs/access.log"
    error_log = "/home/user/app_env/logs/error.log"

    assert os.path.isfile(access_log), f"{access_log} does not exist."
    assert os.path.isfile(error_log), f"{error_log} does not exist."

    with open(access_log, "r") as f:
        access_content = f.read()

    with open(error_log, "r") as f:
        error_content = f.read()

    # Check that redaction occurred
    assert "API_KEY=REDACTED" in access_content, f"Redacted API key not found in {access_log}."
    assert "API_KEY=REDACTED" in error_content, f"Redacted API key not found in {error_log}."

    # Check that original keys are gone
    assert "1234567890abcdef" not in access_content, f"Original 16-char API key still present in {access_log}."
    assert "ABCDEF1234567890" not in error_content, f"Original 16-char API key still present in {error_log}."

    # Check that non-matching keys were NOT redacted
    assert "API_KEY=short" in access_content, f"Short API key was incorrectly redacted in {access_log}."

def test_csp_enforcement():
    app_conf = "/home/user/app_env/config/app.conf"
    assert os.path.isfile(app_conf), f"{app_conf} does not exist."

    expected_line = "Header set Content-Security-Policy \"default-src 'self';\""

    with open(app_conf, "r") as f:
        content = f.read()

    assert expected_line in content, f"CSP header line not found in {app_conf}."

def test_script_is_executable():
    script_path = "/home/user/audit_and_fix.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable by the owner."