# test_final_state.py

import os
import stat
import re
import pytest

def test_app_py_fixed():
    """Verify that app.py unlinks or removes the socket file."""
    app_path = "/home/user/app.py"
    assert os.path.isfile(app_path), f"File {app_path} is missing."
    with open(app_path, "r") as f:
        content = f.read()

    assert "os.unlink(" in content or "os.remove(" in content, "app.py does not seem to unlink or remove the socket file before binding."
    assert 'os.environ.get("TZ") != "Europe/Berlin"' in content, "The timezone check in app.py was removed or altered."

def test_supervisord_conf_updated():
    """Verify supervisord.conf is updated with correct socket, timezone, and autorestart."""
    conf_path = "/home/user/supervisord.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."
    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/app.sock" in content, "supervisord.conf command does not use /home/user/app.sock"
    assert "autorestart=true" in content.lower(), "supervisord.conf does not have autorestart=true"

    # Check for TZ=Europe/Berlin in environment
    assert re.search(r'environment\s*=.*TZ=["\']?Europe/Berlin["\']?', content), "supervisord.conf does not set the environment variable TZ=Europe/Berlin correctly."

def test_supervisord_running():
    """Verify supervisord is running by checking the pidfile."""
    pid_path = "/home/user/supervisord.pid"
    assert os.path.isfile(pid_path), f"supervisord pidfile {pid_path} is missing. Is supervisord running?"

def test_app_sock_exists():
    """Verify the unix socket exists and is a socket."""
    sock_path = "/home/user/app.sock"
    assert os.path.exists(sock_path), f"Socket {sock_path} does not exist."
    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"{sock_path} is not a socket."

def test_success_log():
    """Verify that the success log contains the expected response."""
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()

    assert "HTTP/1.1 200 OK" in content or "Hello from Microservice" in content, "success.log does not contain the expected HTTP response."