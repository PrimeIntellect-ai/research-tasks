# test_final_state.py

import os
import subprocess
import time
import socket
import threading
import hashlib
import pytest
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"data": "success"}')

    def log_message(self, format, *args):
        pass

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """
    Starts the mock backend server and runs the student's deploy.sh script.
    Waits for all required ports to become active.
    """
    # Start mock backend
    server = HTTPServer(('127.0.0.2', 8081), MockBackendHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    # Run deploy.sh
    deploy_script = "/home/user/deploy.sh"
    assert os.path.exists(deploy_script), f"Deployment script missing at {deploy_script}"
    os.chmod(deploy_script, 0o755)

    proc = subprocess.run([deploy_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"deploy.sh failed with return code {proc.returncode}\nStdout: {proc.stdout}\nStderr: {proc.stderr}"

    # Wait for required ports to be listening
    ports = [9000, 8080, 8082]
    for port in ports:
        up = False
        for _ in range(25):
            try:
                with socket.create_connection(('127.0.0.1', port), timeout=0.5):
                    up = True
                    break
            except OSError:
                time.sleep(0.2)
        assert up, f"Port {port} did not become ready after running deploy.sh"

    yield

    server.shutdown()
    server.server_close()

def test_directory_structure_and_symlink():
    """Test that the required configuration files and symlinks are created correctly."""
    secret_path = "/home/user/configs/v2_migrated/secret.txt"
    symlink_path = "/home/user/legacy_system/active"

    assert os.path.exists(secret_path), f"Secret file missing at {secret_path}"
    with open(secret_path, "r") as f:
        content = f.read().strip()
    assert content == "cloud_migration_2024", f"Incorrect secret content: {content}"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    target = os.readlink(symlink_path)
    # The target could be absolute or relative. If relative, resolve it.
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), target))
    assert target == "/home/user/configs/v2_migrated", f"Symlink points to wrong target: {target}"

def test_proxy_invalid_auth():
    """Test that the proxy returns 401 Unauthorized for an invalid token."""
    resp = requests.get("http://127.0.0.1:8080/api/test", headers={"X-Auth-Token": "wrong_token"}, timeout=2)
    assert resp.status_code == 401, f"Expected HTTP 401 for invalid auth, got {resp.status_code}"

    try:
        json_data = resp.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {resp.text}")

    assert json_data == {"error": "unauthorized"}, f"Unexpected JSON response for invalid auth: {json_data}"

def test_proxy_valid_auth():
    """Test that the proxy forwards the request to the backend for a valid token."""
    token = hashlib.sha256(b"cloud_migration_2024").hexdigest()
    resp = requests.get("http://127.0.0.1:8080/api/test", headers={"X-Auth-Token": token}, timeout=2)
    assert resp.status_code == 200, f"Expected HTTP 200 for valid auth, got {resp.status_code}"

    try:
        json_data = resp.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from backend, got: {resp.text}")

    assert json_data == {"data": "success"}, f"Unexpected JSON response for valid auth: {json_data}"

def test_proxy_metrics():
    """Test that the metrics endpoint correctly reports the number of successful authorizations."""
    # Send another valid request to increment the counter
    token = hashlib.sha256(b"cloud_migration_2024").hexdigest()
    requests.get("http://127.0.0.1:8080/api/test", headers={"X-Auth-Token": token}, timeout=2)

    # Test metrics endpoint
    try:
        with socket.create_connection(('127.0.0.1', 8082), timeout=2) as s:
            s.sendall(b"STATS\n")
            data = s.recv(1024).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect or read from metrics endpoint: {e}")

    assert data.startswith("SUCCESS_COUNT: "), f"Metrics response format invalid: {data}"

    try:
        count = int(data.split(":")[1].strip())
    except (IndexError, ValueError):
        pytest.fail(f"Could not parse count from metrics response: {data}")

    assert count >= 2, f"Expected SUCCESS_COUNT >= 2, got {count}"