# test_final_state.py

import os
import stat
import time
import urllib.request
import urllib.error
import subprocess
import pytest

def test_nginx_config_and_process():
    """Verify Nginx config points to the correct socket and Nginx is running."""
    conf_path = "/home/user/nginx/conf/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://unix:/home/user/run/app.sock;" in content, "Nginx config does not point to the correct socket path."

    # Check if Nginx is running
    try:
        subprocess.check_output(["pgrep", "-f", "nginx: master process"])
    except subprocess.CalledProcessError:
        pytest.fail("Nginx master process is not running.")

def test_run_directory_permissions():
    """Verify /home/user/run/ directory exists and has 777 permissions."""
    run_dir = "/home/user/run"
    assert os.path.isdir(run_dir), f"Directory {run_dir} is missing."

    st = os.stat(run_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o777, f"Permissions for {run_dir} are {oct(perms)}, expected 0o777."

def test_app_sh_robustness():
    """Verify app.sh does not use 'exit 1' and returns 403."""
    app_path = "/home/user/app.sh"
    assert os.path.isfile(app_path), f"File {app_path} is missing."

    with open(app_path, "r") as f:
        content = f.read()

    assert "exit 1" not in content, "app.sh still contains the fragile 'exit 1' logic."
    assert "403" in content, "app.sh does not contain a 403 Forbidden response."

def test_supervisor_exists():
    """Verify supervisor.sh exists."""
    supervisor_path = "/home/user/supervisor.sh"
    assert os.path.isfile(supervisor_path), f"File {supervisor_path} is missing."

def test_http_responses():
    """Verify the server returns 200 for normal requests and 403 for BadBot."""
    # Test 200 OK
    req = urllib.request.Request("http://127.0.0.1:8080/")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Normal request failed with HTTP error {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Normal request failed to connect: {e.reason}")

    # Test 403 Forbidden
    req_bot = urllib.request.Request("http://127.0.0.1:8080/")
    req_bot.add_header("User-Agent", "BadBot")
    try:
        with urllib.request.urlopen(req_bot) as response:
            pytest.fail(f"Expected 403 Forbidden, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected 403 Forbidden, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"BadBot request failed to connect: {e.reason}")

def test_supervisor_restarts_daemon():
    """Verify the supervisor restarts the daemon when it is killed."""
    # Ensure socat is running initially
    try:
        subprocess.check_output(["pgrep", "-f", "socat UNIX-LISTEN:/home/user/run/app.sock"])
    except subprocess.CalledProcessError:
        pytest.fail("Socat daemon is not running initially.")

    # Kill socat
    subprocess.call(["pkill", "-f", "socat"])

    # Wait for supervisor to restart it
    time.sleep(3)

    try:
        subprocess.check_output(["pgrep", "-f", "socat UNIX-LISTEN:/home/user/run/app.sock"])
    except subprocess.CalledProcessError:
        pytest.fail("Supervisor failed to restart the daemon after it was killed.")

def test_results_log():
    """Verify results.log contains the correct status codes."""
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "200" in content, "results.log does not contain 200 status code."
    assert "403" in content, "results.log does not contain 403 status code."