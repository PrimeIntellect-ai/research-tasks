# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_task1_vuln_files_log():
    log_path = "/home/user/vuln_files.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_files = {
        "/home/user/auditing_workspace/www/script.js",
        "/home/user/auditing_workspace/www/style.css"
    }

    assert set(lines) == expected_files, f"Log file must contain exactly the world-writable files. Found: {lines}"

def test_task1_permissions():
    www_dir = "/home/user/auditing_workspace/www"
    assert os.path.isdir(www_dir), f"Directory {www_dir} does not exist."

    # Check directory permission
    dir_stat = os.stat(www_dir)
    dir_perm = stat.S_IMODE(dir_stat.st_mode)
    assert dir_perm == 0o755, f"Directory {www_dir} has permissions {oct(dir_perm)}, expected 0o755."

    # Check file permissions
    for root, dirs, files in os.walk(www_dir):
        for d in dirs:
            d_path = os.path.join(root, d)
            d_perm = stat.S_IMODE(os.stat(d_path).st_mode)
            assert d_perm == 0o755, f"Directory {d_path} has permissions {oct(d_perm)}, expected 0o755."
        for f in files:
            f_path = os.path.join(root, f)
            f_perm = stat.S_IMODE(os.stat(f_path).st_mode)
            assert f_perm == 0o644, f"File {f_path} has permissions {oct(f_perm)}, expected 0o644."

def test_task2_csp_header():
    main_rs_path = "/home/user/auditing_workspace/web_server/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} does not exist."

    with open(main_rs_path, "r") as f:
        content = f.read()

    expected_csp = "Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com"
    assert expected_csp in content, "The expected CSP header was not found in main.rs."

    # Check if it's formatted as an HTTP header ending with \r\n
    assert re.search(r"Content-Security-Policy:.*\\r\\n", content) is not None, "CSP header does not appear to be properly inserted in the HTTP header block with \\r\\n."

def test_task2_cargo_build():
    web_server_dir = "/home/user/auditing_workspace/web_server"
    assert os.path.isdir(web_server_dir), f"Directory {web_server_dir} does not exist."

    result = subprocess.run(
        ["cargo", "build"],
        cwd=web_server_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"cargo build failed:\n{result.stderr.decode('utf-8')}"

def test_task3_ssh_hardening():
    sshd_config_path = "/home/user/auditing_workspace/sshd_config_custom"
    assert os.path.isfile(sshd_config_path), f"File {sshd_config_path} does not exist."

    with open(sshd_config_path, "r") as f:
        lines = f.readlines()

    permit_root_login_no = False
    password_auth_no = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if re.match(r"^PermitRootLogin\s+yes", line, re.IGNORECASE):
            pytest.fail("PermitRootLogin is still set to 'yes' (uncommented).")
        if re.match(r"^PasswordAuthentication\s+yes", line, re.IGNORECASE):
            pytest.fail("PasswordAuthentication is still set to 'yes' (uncommented).")

        if re.match(r"^PermitRootLogin\s+no", line, re.IGNORECASE):
            permit_root_login_no = True
        if re.match(r"^PasswordAuthentication\s+no", line, re.IGNORECASE):
            password_auth_no = True

    assert permit_root_login_no, "PermitRootLogin is not explicitly set to 'no'."
    assert password_auth_no, "PasswordAuthentication is not explicitly set to 'no'."