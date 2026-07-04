# test_final_state.py

import os
import json
import re
import pytest

def test_socket_configuration_fixed():
    """
    Verify that either Nginx or Supervisor was updated to communicate over the same UNIX socket.
    """
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    supervisor_conf_path = "/home/user/supervisor/supervisord.conf"

    assert os.path.isfile(nginx_conf_path), f"Nginx config is missing: {nginx_conf_path}"
    assert os.path.isfile(supervisor_conf_path), f"Supervisor config is missing: {supervisor_conf_path}"

    with open(nginx_conf_path, "r") as f:
        nginx_content = f.read()

    with open(supervisor_conf_path, "r") as f:
        supervisor_content = f.read()

    # Check if gunicorn is binding to the socket expected by nginx, or nginx was updated to point to a new socket.
    # The prompt explicitly mentions /home/user/run/app.sock
    socket_path = "/home/user/run/app.sock"

    nginx_has_socket = f"unix:{socket_path}" in nginx_content
    supervisor_has_socket = f"unix:{socket_path}" in supervisor_content or f"bind {socket_path}" in supervisor_content or f"bind=unix:{socket_path}" in supervisor_content.replace(' ', '')

    assert nginx_has_socket and supervisor_has_socket, (
        "Both Nginx and Supervisor must be configured to use the UNIX socket at /home/user/run/app.sock"
    )

def test_git_hook_executable():
    """
    Verify that the post-receive git hook exists and is executable.
    """
    hook_path = "/home/user/cost-data.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook is missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable"

def test_verification_log_content():
    """
    Verify that the verification log exists and contains the correct JSON data.
    """
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Verification log is missing at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content, "Verification log is empty"

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Verification log does not contain valid JSON. Content: {content}")

    assert data.get("status") == "optimized", f"Expected status 'optimized', got {data.get('status')}"
    assert data.get("total") == 150.50, f"Expected total 150.50, got {data.get('total')}"