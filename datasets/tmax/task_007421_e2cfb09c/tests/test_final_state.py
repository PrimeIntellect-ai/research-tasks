# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import socket
import pytest

def test_port_forward_script():
    script_path = '/home/user/port_forward.sh'
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

    with open(script_path, 'r') as f:
        content = f.read().strip()

    assert "socat" in content, f"{script_path} does not contain 'socat' command."
    assert "8080" in content, f"{script_path} does not contain port 8080."
    assert "9000" in content, f"{script_path} does not contain port 9000."

def test_backend_direct_connection():
    # Test if backend is listening on 9000 and responds correctly
    url = "http://127.0.0.1:9000/"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected status 200 on port 9000, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "SYSTEM_OK", f"Expected 'SYSTEM_OK' from backend, got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to backend on port 9000: {e}")

def test_port_forwarding_connection():
    # Test if socat is forwarding 8080 to 9000
    url = "http://127.0.0.1:8080/"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected status 200 on port 8080, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "SYSTEM_OK", f"Expected 'SYSTEM_OK' from forwarded port, got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to forwarded port 8080: {e}")

def test_startup_log_order():
    log_path = '/home/user/startup.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        log_content = f.read()

    db_msg = "DB Mock listening on 5432"
    launch_backend_msg = "Launching backend"
    backend_listen_msg = "Backend service listening on 9000"

    assert db_msg in log_content, f"'{db_msg}' not found in {log_path}"

    db_idx = log_content.find(db_msg)

    launch_backend_idx = log_content.find(launch_backend_msg)
    backend_listen_idx = log_content.find(backend_listen_msg)

    # At least one of the backend messages should be present
    assert launch_backend_idx != -1 or backend_listen_idx != -1, "Backend launch/listen messages not found in log."

    if launch_backend_idx != -1:
        assert db_idx < launch_backend_idx, f"Supervisor did not wait: '{db_msg}' appeared after '{launch_backend_msg}'"

    if backend_listen_idx != -1:
        assert db_idx < backend_listen_idx, f"Supervisor did not wait: '{db_msg}' appeared after '{backend_listen_msg}'"