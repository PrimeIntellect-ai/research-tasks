# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import pytest

WORKSPACE_DIR = "/home/user/workspace"
PID_FILE = os.path.join(WORKSPACE_DIR, "server.pid")
SERVER_EXEC = os.path.join(WORKSPACE_DIR, "server")
SERVER_URL = "http://localhost:8123/verify"

def test_server_pid_running():
    """Verify that the server.pid file exists and the process is running."""
    assert os.path.exists(PID_FILE), f"PID file {PID_FILE} does not exist."
    with open(PID_FILE, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {PID_FILE} does not contain a valid numeric PID (found: {pid_str})."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {PID_FILE}) is not running.")

def test_dynamic_linking():
    """Verify that the server executable dynamically links against libsolver.so."""
    assert os.path.exists(SERVER_EXEC), f"Server executable {SERVER_EXEC} does not exist."

    try:
        output = subprocess.check_output(["ldd", SERVER_EXEC], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running ldd on {SERVER_EXEC} failed: {e.output}")

    assert "libsolver.so" in output, "The server executable is not dynamically linked against libsolver.so."

def test_http_pass_case():
    """Verify the server responds with 200 and pass status for satisfied constraints."""
    data = b"EXPR: libA>=2\nMANIFEST: libA:3"
    req = urllib.request.Request(SERVER_URL, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 but got {e.code}. Response body: {e.read().decode('utf-8')}")
    except Exception as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert status == 200, f"Expected HTTP status 200, got {status}."
    assert '{"status": "pass"}' in body, f"Expected body to contain '{{\"status\": \"pass\"}}', got: {body}"

def test_http_fail_case():
    """Verify the server responds with 400 and fail status for unsatisfied constraints."""
    data = b"EXPR: libA>=2,libB==2\nMANIFEST: libA:3,libB:1"
    req = urllib.request.Request(SERVER_URL, data=data, method="POST")

    status = None
    body = ""
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert status == 400, f"Expected HTTP status 400, got {status}."
    assert '{"status": "fail"}' in body, f"Expected body to contain '{{\"status\": \"fail\"}}', got: {body}"