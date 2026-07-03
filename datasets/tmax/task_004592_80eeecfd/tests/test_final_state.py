# test_final_state.py

import os
import stat
import hashlib
import sys

def test_cracked_password():
    password_file = "/home/user/cracked_password.txt"
    assert os.path.isfile(password_file), f"The file {password_file} does not exist."
    with open(password_file, "r") as f:
        content = f.read().strip()
    assert content == "sunshine", f"The cracked password file should contain exactly 'sunshine', but contains '{content}'."

def test_login_py_behavior():
    login_file = "/home/user/app/login.py"
    assert os.path.isfile(login_file), f"The file {login_file} does not exist."

    # Import the module
    sys.path.append('/home/user/app')
    try:
        from login import get_redirect_url
    except ImportError:
        assert False, "Could not import get_redirect_url from /home/user/app/login.py"

    # Test cases
    assert get_redirect_url('/dashboard') == '/dashboard', "Failed on valid relative path"
    assert get_redirect_url('//evil.com') == '/home', "Failed on protocol-relative path"
    assert get_redirect_url('https://evil.com') == '/home', "Failed on absolute URL"
    assert get_redirect_url(None) == '/home', "Failed on None"
    assert get_redirect_url('') == '/home', "Failed on empty string"

def test_config_json_permissions():
    config_file = "/home/user/app/config.json"
    assert os.path.isfile(config_file), f"The file {config_file} does not exist."

    st = os.stat(config_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"The file {config_file} must have permissions 600, but has {oct(perms)}."

def test_audit_log():
    audit_log = "/home/user/audit_log.txt"
    login_file = "/home/user/app/login.py"

    assert os.path.isfile(audit_log), f"The file {audit_log} does not exist."
    assert os.path.isfile(login_file), f"The file {login_file} does not exist."

    with open(login_file, "rb") as f:
        login_content = f.read()
    expected_hash = hashlib.sha256(login_content).hexdigest()

    with open(audit_log, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 3, f"The audit log must have exactly 3 lines, but found {len(lines)}."
    assert lines[0] == "sunshine", f"Line 1 of audit log should be 'sunshine', but is '{lines[0]}'."
    assert lines[1] == "600", f"Line 2 of audit log should be '600', but is '{lines[1]}'."
    assert lines[2] == expected_hash, f"Line 3 of audit log should be the SHA256 hash of login.py ({expected_hash}), but is '{lines[2]}'."