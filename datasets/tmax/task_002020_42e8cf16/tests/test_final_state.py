# test_final_state.py

import os
import subprocess
import ssl
import urllib.request
import pytest

def test_c_file_modified():
    c_file = "/home/user/account_monitor.c"
    assert os.path.isfile(c_file), f"File {c_file} is missing."
    with open(c_file, "r") as f:
        content = f.read()
    assert "/home/user/users.db" in content, "Absolute path '/home/user/users.db' missing in account_monitor.c."
    assert "/home/user/public_html/report.html" in content, "Absolute path '/home/user/public_html/report.html' missing in account_monitor.c."

def test_binary_compiled():
    bin_file = "/home/user/account_monitor"
    assert os.path.isfile(bin_file), f"Compiled binary {bin_file} is missing."
    assert os.access(bin_file, os.X_OK), f"File {bin_file} is not executable."

def test_expect_script_exists():
    exp_file = "/home/user/add_user.exp"
    assert os.path.isfile(exp_file), f"Expect script {exp_file} is missing."
    with open(exp_file, "r") as f:
        content = f.read()
    assert "spawn" in content, "Expect script does not contain 'spawn'."
    assert "expect" in content, "Expect script does not contain 'expect'."

def test_user_added():
    db_file = "/home/user/users.db"
    assert os.path.isfile(db_file), f"Database file {db_file} is missing."
    with open(db_file, "r") as f:
        content = f.read()
    assert "charlie" in content, "User 'charlie' was not added to users.db."

def test_tls_certs_exist():
    cert_file = "/home/user/certs/cert.pem"
    key_file = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_file), f"Certificate file {cert_file} is missing."
    assert os.path.isfile(key_file), f"Key file {key_file} is missing."

def test_systemd_service_active():
    service_file = "/home/user/.config/systemd/user/monitor-web.service"
    assert os.path.isfile(service_file), f"Systemd service file {service_file} is missing."

    # Check if service is active
    env = os.environ.copy()
    env["XDG_RUNTIME_DIR"] = "/run/user/1000"  # Assuming standard user ID 1000 for 'user'
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "monitor-web.service"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            check=True
        )
        assert result.stdout.strip() == "active", "monitor-web.service is not active."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"systemctl --user is-active monitor-web.service failed. Output: {e.stdout.strip()} {e.stderr.strip()}")

def test_web_server_running_and_report_generated():
    url = "https://localhost:8443/report.html"

    # Create an SSL context that ignores self-signed certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            content = response.read().decode('utf-8')
            assert "charlie" in content, "User 'charlie' not found in the generated report.html served by the web server."
    except Exception as e:
        pytest.fail(f"Failed to fetch {url}: {e}")