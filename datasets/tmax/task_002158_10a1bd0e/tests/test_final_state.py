# test_final_state.py

import os
import time
import json
import base64
import subprocess
import urllib.request
import urllib.error
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

def sign(payload: str) -> str:
    reversed_str = payload[::-1]
    xored_bytes = bytes([ord(c) ^ 0x3F for c in reversed_str])
    return base64.b64encode(xored_bytes).decode('utf-8')

class DummyBackendHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        headers_dict = {f"HTTP_{k.upper().replace('-', '_')}": v for k, v in self.headers.items()}
        self.wfile.write(json.dumps(headers_dict).encode('utf-8'))

@pytest.fixture(scope="module")
def dummy_backend():
    server = HTTPServer(('127.0.0.1', 9000), DummyBackendHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    server.server_close()

@pytest.fixture(scope="module")
def user_proxy():
    proxy_script = "/home/user/proxy.py"
    assert os.path.exists(proxy_script), f"Proxy script not found at {proxy_script}"

    p = subprocess.Popen(["python3", proxy_script])

    # Wait for proxy to start
    started = False
    for _ in range(20):
        try:
            urllib.request.urlopen("http://127.0.0.1:8080/", timeout=0.1)
            started = True
            break
        except Exception:
            time.sleep(0.1)

    yield p
    p.terminate()
    p.wait()

def test_proxy_accuracy_and_performance(dummy_backend, user_proxy):
    success = 0
    total_requests = 2000

    start_time = time.time()
    for i in range(total_requests):
        uri = f"/api/test?id={i}"
        try:
            req = urllib.request.Request(f"http://127.0.0.1:8080{uri}")
            with urllib.request.urlopen(req, timeout=1.0) as response:
                data = json.loads(response.read().decode('utf-8'))
                sig = data.get("HTTP_X_CUSTOM_SIGNATURE")

                expected = sign(uri)
                if sig == expected:
                    success += 1
        except Exception as e:
            pass # Request failed, will be caught by accuracy check

    end_time = time.time()
    time_taken = end_time - start_time
    accuracy = success / total_requests

    assert accuracy == 1.0, f"Accuracy is {accuracy}, expected 1.0 (some signatures mismatched or requests failed)"
    assert time_taken <= 1.5, f"Performance threshold failed: time taken {time_taken:.3f}s > 1.5s"