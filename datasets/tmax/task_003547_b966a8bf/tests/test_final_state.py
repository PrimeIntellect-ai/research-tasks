# test_final_state.py

import os
import stat
import pytest

def test_scripts_exist_and_executable():
    analyze_script = "/home/user/analyze.sh"
    isolation_script = "/home/user/run_isolation.sh"

    # Check analyze.sh
    assert os.path.exists(analyze_script), f"{analyze_script} does not exist."
    assert os.path.isfile(analyze_script), f"{analyze_script} is not a file."
    st = os.stat(analyze_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{analyze_script} is not executable."

    # Check run_isolation.sh
    assert os.path.exists(isolation_script), f"{isolation_script} does not exist."
    assert os.path.isfile(isolation_script), f"{isolation_script} is not a file."
    st = os.stat(isolation_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{isolation_script} is not executable."

def test_isolation_script_content():
    isolation_script = "/home/user/run_isolation.sh"
    with open(isolation_script, 'r') as f:
        content = f.read()

    assert "unshare" in content, f"{isolation_script} does not use the 'unshare' command."
    # Check for user and network isolation flags
    has_user_flag = "-r" in content or "--map-root-user" in content or "-U" in content or "--user" in content
    has_net_flag = "-n" in content or "--net" in content
    assert has_user_flag and has_net_flag, f"{isolation_script} must use unshare with user and network isolation flags (e.g., -r -n)."

def test_audit_trail_content():
    audit_trail = "/home/user/audit_trail.csv"
    assert os.path.exists(audit_trail), f"{audit_trail} does not exist."
    assert os.path.isfile(audit_trail), f"{audit_trail} is not a file."

    expected_lines = [
        "LOG-001,XSS,True,<script>alert(1)</script>",
        "LOG-002,None,False,SELECT * FROM users;",
        "LOG-003,SQLi,False,' OR 1=1 --",
        "LOG-004,None,False,hello world",
        "LOG-005,XSS,True,<img src=x onerror=alert(1)>",
        "LOG-006,SQLi,False,UNION SELECT username, password FROM admins"
    ]

    with open(audit_trail, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {audit_trail} do not match the expected audit trail."