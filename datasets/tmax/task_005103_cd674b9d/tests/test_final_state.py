# test_final_state.py

import os
import re
import stat
import pytest
import requests
import time

def get_expected_upstream_port():
    log_path = "/app/provision_events.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        lines = f.readlines()

    port = None
    for line in reversed(lines):
        match = re.search(r'\[ROUTING_UPDATE\] NEW_UPSTREAM_PORT=(\d+)', line)
        if match:
            port = match.group(1)
            break

    assert port is not None, "Could not find NEW_UPSTREAM_PORT in provision_events.log"
    return port

def test_upstream_conf_content():
    expected_port = get_expected_upstream_port()
    conf_path = "/home/user/upstream.conf"

    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read().strip()

    assert content == expected_port, f"Expected {conf_path} to contain '{expected_port}', but found '{content}'."

def test_router_binary_exists_and_executable():
    bin_path = "/home/user/router"
    assert os.path.isfile(bin_path), f"{bin_path} does not exist."

    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{bin_path} is not executable."

    with open(bin_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{bin_path} is not a valid ELF binary."

def test_start_router_script_exists():
    script_path = "/home/user/start_router.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_proxy_service_running_and_forwarding():
    # The proxy should be listening on 127.0.0.1:8080 and forwarding to the backend.
    url = "http://127.0.0.1:8080/health"

    max_retries = 3
    last_exception = None

    for _ in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status") == "provisioned":
                        return # Success
                except ValueError:
                    pass
            last_exception = f"Status code: {response.status_code}, Body: {response.text}"
        except requests.exceptions.RequestException as e:
            last_exception = str(e)

        time.sleep(1)

    pytest.fail(f"Failed to verify proxy service at {url}. Last error: {last_exception}")