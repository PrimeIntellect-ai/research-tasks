# test_final_state.py

import os
import glob
import subprocess
import threading
import urllib.request
import urllib.error
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

class MockBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BACKEND_OK")
    def log_message(self, format, *args):
        pass

@pytest.fixture(scope="module")
def mock_backend():
    server = HTTPServer(('127.0.0.1', 9000), MockBackendHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield
    server.shutdown()
    server.server_close()

def test_detect_script_adversarial_corpus():
    script_path = "/home/user/detect.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    evil_dir = "/home/user/corpora/evil/"
    clean_dir = "/home/user/corpora/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    for e_file in evil_files:
        result = subprocess.run([script_path, e_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(e_file))

    clean_modified = []
    for c_file in clean_files:
        result = subprocess.run([script_path, c_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(c_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus failed:\n" + "\n".join(errors)

def test_nginx_routing_and_filtering(mock_backend):
    # Wait a moment to ensure Nginx and backend are up
    time.sleep(1)

    # Test 1: Normal request should route to backend and return 200
    req = urllib.request.Request("http://127.0.0.1:8080/api/test")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            body = response.read()
            assert b"BACKEND_OK" in body, "Response did not come from the mock backend."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Normal request to /api/test failed with HTTP error: {e.code}")
    except Exception as e:
        pytest.fail(f"Normal request to /api/test failed: {e}")

    # Test 2: Request with X-Debug-Bypass: true should return 403
    req_bypass = urllib.request.Request("http://127.0.0.1:8080/api/test")
    req_bypass.add_header("X-Debug-Bypass", "true")
    try:
        with urllib.request.urlopen(req_bypass, timeout=5) as response:
            pytest.fail(f"Expected 403 Forbidden for bypass header, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected 403 Forbidden for bypass header, got {e.code}"
    except Exception as e:
        pytest.fail(f"Bypass request failed with unexpected error: {e}")