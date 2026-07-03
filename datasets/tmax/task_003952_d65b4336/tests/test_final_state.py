# test_final_state.py
import os
import re
import requests
import subprocess
import time

def test_route_h_content():
    path = "/app/legacy-svc/route.h"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    expected = '#define ROUTE_PATH "/api/v1/system/health"'
    assert content == expected, f"Expected {path} to contain exactly '{expected}', but got '{content}'"

def test_server_binary_compiled():
    path = "/app/legacy-svc/server"
    assert os.path.isfile(path), f"Compiled binary {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_logrotate_conf():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # Check for the log file path
    assert "/home/user/app.log" in content, f"Expected '/home/user/app.log' in {path}"

    # Check for required directives
    directives = ["daily", "rotate 3", "compress", "missingok", "size 10M"]
    # Normalize whitespace for flexible matching
    normalized_content = re.sub(r'\s+', ' ', content)

    for directive in directives:
        # For size 10M, allow variations like size=10M or size 10M
        if directive == "size 10M":
            assert re.search(r'size\s*=?\s*10M', content, re.IGNORECASE), f"Expected 'size 10M' directive in {path}"
        elif directive == "rotate 3":
            assert re.search(r'rotate\s+3', content), f"Expected 'rotate 3' directive in {path}"
        else:
            assert re.search(r'\b' + directive + r'\b', content), f"Expected '{directive}' directive in {path}"

def test_service_and_port_forwarding():
    # The multi-protocol verifier requires an HTTP GET request to 127.0.0.1:9090/api/v1/system/health
    url = "http://127.0.0.1:9090/api/v1/system/health"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service at {url}. Is the server and socat port forwarding running? Error: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Expected JSON response, got: {response.text}"

    assert data == {"status": "ok"}, f"Expected response body {{'status': 'ok'}}, got {data}"

def test_processes_running():
    # Verify both server and socat processes are running in the background
    try:
        ps_output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        assert False, "Failed to execute 'ps aux'"

    assert "server" in ps_output or "./server" in ps_output, "The 'server' process does not appear to be running."
    assert "socat" in ps_output, "The 'socat' process does not appear to be running."