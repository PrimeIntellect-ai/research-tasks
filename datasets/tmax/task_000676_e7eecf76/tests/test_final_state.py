# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.exists(report_path), f"Audit report not found at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a file"

    with open(report_path, "r") as f:
        content = f.read().splitlines()

    expected_token = "Token: B4ckd00r_T0k3n_9921"
    expected_suid = "SUID: /home/user/old_backup_tool"

    assert expected_token in content, f"Expected '{expected_token}' in {report_path}"
    assert expected_suid in content, f"Expected '{expected_suid}' in {report_path}"

def test_secure_net_helper_permissions():
    binary_path = "/home/user/secure_net_helper"
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.path.isfile(binary_path), f"{binary_path} is not a file"

    st = os.stat(binary_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o500, f"Permissions for {binary_path} are {oct(perms)}, expected 0o500"

def test_secure_net_helper_functionality():
    binary_path = "/home/user/secure_net_helper"
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}"

    # Test with "admin"
    result_admin = subprocess.run([binary_path, "admin"], capture_output=True, text=True)
    assert "ACCESS GRANTED" in result_admin.stdout, "Expected 'ACCESS GRANTED' when argument is 'admin'"

    # Test with "hacker"
    result_other = subprocess.run([binary_path, "hacker"], capture_output=True, text=True)
    assert "ACCESS DENIED" in result_other.stdout, "Expected 'ACCESS DENIED' when argument is not 'admin'"

    # Test with no arguments
    result_none = subprocess.run([binary_path], capture_output=True, text=True)
    assert "ACCESS DENIED" in result_none.stdout, "Expected 'ACCESS DENIED' when no arguments are provided"