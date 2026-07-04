# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_cracked_password():
    path = "/home/user/cracked_password.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "hunter2", f"Expected cracked password to be 'hunter2', but got '{content}'"

def test_vuln_headers():
    path = "/home/user/vuln_headers.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "Location: http://evil.com" in content, "Expected 'Location: http://evil.com' in vuln_headers.txt"
    assert "Status: 302 Found" in content, "Expected 'Status: 302 Found' in vuln_headers.txt"

def test_login_cgi_patched():
    path = "/home/user/app/login.cgi"
    assert os.path.isfile(path), f"Missing file: {path}"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

    env = os.environ.copy()
    env["QUERY_STRING"] = "user=admin&pass=hunter2&redirect=http://evil.com"

    result = subprocess.run([path], env=env, capture_output=True, text=True)

    assert "Location: /dashboard" in result.stdout, "Script did not override malicious redirect to /dashboard"
    assert "Location: http://evil.com" not in result.stdout, "Script still vulnerable to open redirect"

def test_passwd_db_permissions():
    path = "/home/user/app/passwd.db"
    assert os.path.isfile(path), f"Missing file: {path}"

    st = os.stat(path)
    mode = stat.S_IMODE(st.st_mode)

    assert mode == 0o600, f"Expected permissions to be 600, but got {oct(mode)}"

def test_ssh_config_hardened():
    path = "/home/user/ssh_config"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    permit_root_login = re.search(r"^\s*PermitRootLogin\s+no\s*$", content, re.MULTILINE)
    password_auth = re.search(r"^\s*PasswordAuthentication\s+no\s*$", content, re.MULTILINE)

    assert permit_root_login, "Expected 'PermitRootLogin no' directive in ssh_config"
    assert password_auth, "Expected 'PasswordAuthentication no' directive in ssh_config"

    permit_root_login_yes = re.search(r"^\s*PermitRootLogin\s+yes\s*$", content, re.MULTILINE)
    password_auth_yes = re.search(r"^\s*PasswordAuthentication\s+yes\s*$", content, re.MULTILINE)

    assert not permit_root_login_yes, "Insecure 'PermitRootLogin yes' directive still present"
    assert not password_auth_yes, "Insecure 'PasswordAuthentication yes' directive still present"