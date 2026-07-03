# test_final_state.py

import os
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = '/home/user/ws_proxy/Makefile'
    assert os.path.isfile(makefile_path), f"The file {makefile_path} does not exist."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "-lws_v2" in content, "Makefile does not link against the correct libws version (-lws_v2)."
    assert "-lauth_v3" in content, "Makefile does not link against the correct libauth version (-lauth_v3)."
    assert "-lfilter_v2" in content, "Makefile does not link against the correct libfilter version (-lfilter_v2)."

def test_proxy_server_built():
    executable_path = '/home/user/ws_proxy/proxy_server'
    assert os.path.isfile(executable_path), f"The executable {executable_path} was not built."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_ws_response_log_content():
    log_path = '/home/user/ws_response.log'
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = '{"status": "blocked", "reason": "XSS detected"}'
    assert content == expected_content, f"The log file content is incorrect. Expected '{expected_content}', got '{content}'."

def test_proxy_server_running():
    # Check if the proxy server process is running
    try:
        output = subprocess.check_output(['pgrep', '-f', 'proxy_server']).decode('utf-8').strip()
        assert output, "The proxy_server process is not running in the background."
    except subprocess.CalledProcessError:
        pytest.fail("The proxy_server process is not running in the background.")