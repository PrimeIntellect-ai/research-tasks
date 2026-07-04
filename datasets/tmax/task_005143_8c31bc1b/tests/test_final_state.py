# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import pytest

def test_start_app_sh_fixed():
    path = "/home/user/app/start_app.sh"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "/home/user/app" in content, "start_app.sh does not seem to change to or reference the correct directory."

def test_nginx_conf_fixed():
    path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "proxy_pass http://unix:/home/user/app/app.sock;" in content, "Nginx config proxy_pass is not pointing to the correct socket."
    assert "403" in content, "Nginx config does not seem to contain a 403 rule for /admin."

def test_rotate_logs_script_exists():
    path = "/home/user/app/rotate_logs.py"
    assert os.path.isfile(path), f"Log rotation script missing: {path}"

def test_log_files_exist_and_permissions():
    log_path = "/home/user/app/app.log"
    archive_path = "/home/user/app/app.log.archive"

    assert os.path.isfile(archive_path), f"Archive log missing: {archive_path}"
    assert os.path.isfile(log_path), f"New log file missing: {log_path}"

    st = os.stat(log_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o644, f"Permissions for {log_path} are {oct(perms)}, expected 0o644"

def test_socket_exists():
    sock_path = "/home/user/app/app.sock"
    assert os.path.exists(sock_path), f"Socket missing: {sock_path}"
    assert stat.S_ISSOCK(os.stat(sock_path).st_mode), f"Path {sock_path} is not a socket"

def test_http_root_returns_success():
    url = "http://127.0.0.1:8080/"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert status == 200, f"Expected status 200, got {status}"
    assert "Hello from Python app!" in body, "Response body does not contain the expected text."

def test_http_admin_returns_403():
    url = "http://127.0.0.1:8080/admin"
    try:
        req = urllib.request.Request(url)
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Expected a 403 Forbidden error, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected status 403, got {e.code}"
    except Exception as e:
        pytest.fail(f"Unexpected error when connecting to {url}: {e}")