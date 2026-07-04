# test_final_state.py
import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import pytest

PROXY_PORT = 8080
APP_1_PORT = 8081
APP_2_PORT = 8082
MONITOR_PORT = 9090
AUTH_TOKEN = "SecretMonitor77"
THRESHOLD = 4

class MockBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/fail":
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Success from {self.server.server_port} for {self.path}".encode())

    def log_message(self, format, *args):
        pass

def run_mock_server(port):
    server = HTTPServer(('127.0.0.1', port), MockBackendHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

@pytest.fixture(scope="module", autouse=True)
def setup_mock_backends():
    server1 = run_mock_server(APP_1_PORT)
    server2 = run_mock_server(APP_2_PORT)
    time.sleep(1)
    yield
    server1.shutdown()
    server2.shutdown()

def test_directories_and_symlink():
    assert os.path.isdir("/home/user/telemetry/logs/"), "Directory /home/user/telemetry/logs/ does not exist."
    assert os.path.isdir("/home/user/telemetry/config/"), "Directory /home/user/telemetry/config/ does not exist."
    assert os.path.islink("/home/user/active_logs"), "Symlink /home/user/active_logs does not exist."
    assert os.readlink("/home/user/active_logs") == "/home/user/telemetry/logs/", "Symlink /home/user/active_logs does not point to /home/user/telemetry/logs/."

def test_proxy_routing():
    try:
        resp1 = requests.get(f"http://127.0.0.1:{PROXY_PORT}/app1/testdata", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy on port {PROXY_PORT}: {e}")

    assert resp1.status_code == 200, f"Expected 200 from proxy app1, got {resp1.status_code}"
    assert "Success from 8081 for /testdata" in resp1.text, f"Unexpected response from app1 proxy: {resp1.text}"

    try:
        resp2 = requests.get(f"http://127.0.0.1:{PROXY_PORT}/app2/info", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy on port {PROXY_PORT}: {e}")

    assert resp2.status_code == 200, f"Expected 200 from proxy app2, got {resp2.status_code}"
    assert "Success from 8082 for /info" in resp2.text, f"Unexpected response from app2 proxy: {resp2.text}"

def test_monitoring_api():
    try:
        resp = requests.get(f"http://127.0.0.1:{MONITOR_PORT}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to monitoring API on port {MONITOR_PORT}: {e}")
    assert resp.status_code == 401, f"Expected 401 for no auth, got {resp.status_code}"

    resp = requests.get(f"http://127.0.0.1:{MONITOR_PORT}/health", headers={"Authorization": "Bearer WrongToken"}, timeout=5)
    assert resp.status_code == 401, f"Expected 401 for wrong auth, got {resp.status_code}"

    resp = requests.get(f"http://127.0.0.1:{MONITOR_PORT}/health", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, timeout=5)
    assert resp.status_code == 200, f"Expected 200 for OK state, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Monitoring API did not return valid JSON: {resp.text}")
    assert data.get("alert_status") == "OK", f"Expected alert_status OK, got {data}"

    for _ in range(5):
        requests.get(f"http://127.0.0.1:{PROXY_PORT}/app1/fail", timeout=5)

    time.sleep(1)

    resp = requests.get(f"http://127.0.0.1:{MONITOR_PORT}/health", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, timeout=5)
    assert resp.status_code == 503, f"Expected 503 for CRITICAL state, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Monitoring API did not return valid JSON: {resp.text}")
    assert data.get("alert_status") == "CRITICAL", f"Expected alert_status CRITICAL, got {data}"