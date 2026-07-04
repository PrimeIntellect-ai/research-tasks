# test_final_state.py

import threading
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import time
import pytest
import os

class MockUpstreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Mock Upstream OK")
    def log_message(self, format, *args):
        pass # Suppress logging

@pytest.fixture(scope="module", autouse=True)
def mock_upstream_server():
    server_address = ('127.0.0.1', 8443)
    httpd = HTTPServer(server_address, MockUpstreamHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    crt_file = "/app/server.crt"
    key_file = "/app/server.key"

    if not os.path.exists(crt_file):
        for f in os.listdir("/app"):
            if f.endswith(".crt") and f != "ca.crt":
                crt_file = os.path.join("/app", f)
                key_file = crt_file.replace(".crt", ".key")
                if not os.path.exists(key_file):
                    key_file = os.path.join("/app", "server.key") # fallback
                break

    context.load_cert_chain(certfile=crt_file, keyfile=key_file)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    # Give the server a moment to start
    time.sleep(1)

    yield

    httpd.shutdown()

def test_proxy_valid_relative_redirect():
    url = "http://127.0.0.1:9090/?next=/profile"
    headers = {"Authorization": "Bearer 82045"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid relative redirect, got {response.status_code}. Response: {response.text}"

def test_proxy_valid_absolute_redirect():
    url = "http://127.0.0.1:9090/?next=https://internal-corp.local/admin"
    headers = {"Authorization": "Bearer 82045"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid absolute redirect to internal-corp.local, got {response.status_code}. Response: {response.text}"

def test_proxy_invalid_redirect_evil_com():
    url = "http://127.0.0.1:9090/?next=http://evil.com/login"
    headers = {"Authorization": "Bearer 82045"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")

    assert response.status_code == 403, f"Expected 403 Forbidden for redirect to evil.com, got {response.status_code}. Response: {response.text}"

def test_proxy_invalid_redirect_protocol_relative():
    url = "http://127.0.0.1:9090/?next=//evil.com/login"
    headers = {"Authorization": "Bearer 82045"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")

    assert response.status_code == 403, f"Expected 403 Forbidden for protocol-relative redirect to evil.com, got {response.status_code}. Response: {response.text}"

def test_proxy_invalid_token():
    url = "http://127.0.0.1:9090/?next=/profile"
    headers = {"Authorization": "Bearer 99999"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect token, got {response.status_code}. Response: {response.text}"

def test_proxy_missing_token():
    url = "http://127.0.0.1:9090/?next=/profile"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}. Response: {response.text}"