# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import pytest

def test_wrapper_fix():
    wrapper_path = '/home/user/run_wrapper.sh'
    log_file = '/home/user/logs/restore.log'

    # Remove log file if it exists to ensure the wrapper actually creates it
    if os.path.exists(log_file):
        os.remove(log_file)

    # Execute the wrapper script
    result = subprocess.run(['bash', wrapper_path], capture_output=True, text=True)

    # Check if log file was created
    assert os.path.isfile(log_file), (
        f"Wrapper script failed to create {log_file}. "
        f"Stdout: {result.stdout}, Stderr: {result.stderr}"
    )

    with open(log_file, 'r') as f:
        content = f.read()

    assert "SUCCESS" in content, (
        f"Log file {log_file} does not contain 'SUCCESS'. "
        f"Actual content: {content}"
    )

class DummyBackendHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b'BACKEND_DATA')

@pytest.fixture(scope="module")
def backend_server():
    server = HTTPServer(('127.0.0.1', 8080), DummyBackendHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    server.server_close()
    thread.join()

@pytest.fixture(scope="module")
def proxy_server():
    proxy_path = '/home/user/health_proxy.py'
    assert os.path.isfile(proxy_path), f"Proxy script {proxy_path} does not exist."

    # Start the proxy server
    proc = subprocess.Popen(['python3', proxy_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give it a moment to start
    time.sleep(2)

    # Check if it crashed immediately
    if proc.poll() is not None:
        stdout, stderr = proc.communicate()
        pytest.fail(f"Proxy server crashed on startup. Stderr: {stderr.decode()}")

    yield proc

    proc.terminate()
    proc.wait(timeout=5)

def test_health_proxy_success(proxy_server, backend_server):
    # Ensure the log file is in the success state
    log_file = '/home/user/logs/restore.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'w') as f:
        f.write("RESTORE JOB: SUCCESS\n")

    req = urllib.request.Request("http://127.0.0.1:9090/health")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "OK", f"Expected body 'OK', got '{body}'"
    except urllib.error.HTTPError as e:
        pytest.fail(f"/health endpoint returned error: {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

def test_health_proxy_failure(proxy_server):
    # Simulate missing or failing log
    log_file = '/home/user/logs/restore.log'
    backup_log = '/home/user/logs/restore.log.bak'

    if os.path.exists(log_file):
        os.rename(log_file, backup_log)

    try:
        req = urllib.request.Request("http://127.0.0.1:9090/health")
        try:
            urllib.request.urlopen(req, timeout=5)
            pytest.fail("Expected 503 error, but request succeeded.")
        except urllib.error.HTTPError as e:
            assert e.code == 503, f"Expected status 503, got {e.code}"
            body = e.read().decode('utf-8').strip()
            assert body == "FAIL", f"Expected body 'FAIL', got '{body}'"
    finally:
        # Restore the log file
        if os.path.exists(backup_log):
            os.rename(backup_log, log_file)

def test_health_proxy_forwarding(proxy_server, backend_server):
    req = urllib.request.Request("http://127.0.0.1:9090/api/status")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 201, f"Expected status 201 from backend, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "BACKEND_DATA", f"Expected body 'BACKEND_DATA', got '{body}'"
    except urllib.error.HTTPError as e:
        if e.code == 201:
            body = e.read().decode('utf-8').strip()
            assert body == "BACKEND_DATA", f"Expected body 'BACKEND_DATA', got '{body}'"
        else:
            pytest.fail(f"Forwarding failed with error: {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to connect to forwarded endpoint: {e}")