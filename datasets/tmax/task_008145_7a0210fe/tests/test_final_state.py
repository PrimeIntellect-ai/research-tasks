# test_final_state.py

import os
import stat
import subprocess
import pytest
import re

NGINX_CONF_PATH = "/home/user/app/nginx.conf"
BACKEND_ENV_PATH = "/home/user/app/backend.env"
MONITOR_SCRIPT_PATH = "/home/user/monitor.sh"
METRICS_LOG_PATH = "/home/user/app/metrics.log"
EXPECTED_SOCKET_PATH = "/home/user/run/production_backend.sock"

def test_nginx_conf_updated():
    assert os.path.exists(NGINX_CONF_PATH), f"{NGINX_CONF_PATH} does not exist."
    with open(NGINX_CONF_PATH, "r") as f:
        content = f.read()

    expected_directive = f"proxy_pass http://unix:{EXPECTED_SOCKET_PATH};"
    assert expected_directive in content, f"Nginx configuration was not updated correctly. Expected to find: {expected_directive}"

def test_monitor_script_exists_and_executable():
    assert os.path.exists(MONITOR_SCRIPT_PATH), f"{MONITOR_SCRIPT_PATH} does not exist."
    st = os.stat(MONITOR_SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{MONITOR_SCRIPT_PATH} is not executable."

def test_monitor_script_healthy_behavior():
    # Ensure the metrics log is clean or we can track new lines
    if os.path.exists(METRICS_LOG_PATH):
        os.remove(METRICS_LOG_PATH)

    # Run the script
    result = subprocess.run([MONITOR_SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Monitor script failed to execute. stderr: {result.stderr}"

    assert os.path.exists(METRICS_LOG_PATH), f"Monitor script did not create/write to {METRICS_LOG_PATH}."

    with open(METRICS_LOG_PATH, "r") as f:
        log_content = f.read().strip().split('\n')

    expected_log = f"STATUS: HEALTHY - {EXPECTED_SOCKET_PATH}"
    assert expected_log in log_content, f"Expected '{expected_log}' in {METRICS_LOG_PATH}, but got: {log_content}"

def test_monitor_script_unhealthy_behavior():
    # Temporarily change nginx.conf to point to a non-existent socket
    fake_socket = "/home/user/run/non_existent.sock"

    with open(NGINX_CONF_PATH, "r") as f:
        original_conf = f.read()

    modified_conf = re.sub(r'proxy_pass http://unix:.*?;', f'proxy_pass http://unix:{fake_socket};', original_conf)

    try:
        with open(NGINX_CONF_PATH, "w") as f:
            f.write(modified_conf)

        # Run the script
        result = subprocess.run([MONITOR_SCRIPT_PATH], capture_output=True, text=True)
        assert result.returncode == 0, f"Monitor script failed to execute during unhealthy test. stderr: {result.stderr}"

        with open(METRICS_LOG_PATH, "r") as f:
            log_content = f.read().strip().split('\n')

        expected_log = f"STATUS: UNHEALTHY - {fake_socket}"
        assert expected_log in log_content, f"Expected '{expected_log}' in {METRICS_LOG_PATH} for missing socket, but got: {log_content}"

    finally:
        # Restore original conf
        with open(NGINX_CONF_PATH, "w") as f:
            f.write(original_conf)