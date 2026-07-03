# test_final_state.py

import os
import stat
import json
import subprocess
import re
import pytest

def test_rust_vulnerability_fixed():
    main_rs = "/home/user/web_service/src/main.rs"
    assert os.path.isfile(main_rs), f"Missing {main_rs}"

    with open(main_rs, "r") as f:
        content = f.read()
        assert "Invalid filename" in content, "The Rust code does not contain the expected error message 'Invalid filename' for path traversal attempts."
        assert "/" in content or ".." in content, "The Rust code does not seem to check for '/' or '..'."

    # Run cargo test
    result = subprocess.run(
        ["cargo", "test"],
        cwd="/home/user/web_service",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\n{result.stdout}\n{result.stderr}"

def test_ssh_hardening():
    ssh_config = "/home/user/ssh_audit/sshd_config"
    assert os.path.isfile(ssh_config), f"Missing {ssh_config}"

    with open(ssh_config, "r") as f:
        content = f.read()

    # Check PermitRootLogin
    assert re.search(r"(?m)^[ \t]*PermitRootLogin[ \t]+no[ \t]*$", content), "PermitRootLogin is not strictly set to 'no' in sshd_config."

    # Check PasswordAuthentication
    assert re.search(r"(?m)^[ \t]*PasswordAuthentication[ \t]+no[ \t]*$", content), "PasswordAuthentication is not strictly set to 'no' in sshd_config."

def test_ssh_key_permissions():
    ssh_key = "/home/user/ssh_keys/id_rsa"
    assert os.path.isfile(ssh_key), f"Missing {ssh_key}"

    file_stat = os.stat(ssh_key)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o600, f"Expected permissions 0o600 for {ssh_key}, got {oct(permissions)}"

def test_audit_report():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Missing {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert report.get("identified_cwe") == "CWE-22", "identified_cwe must be exactly 'CWE-22'."
    assert report.get("ssh_root_login_fixed") is True, "ssh_root_login_fixed must be true."
    assert report.get("ssh_password_auth_fixed") is True, "ssh_password_auth_fixed must be true."
    assert report.get("key_permission_octal") == "0600", "key_permission_octal must be '0600'."