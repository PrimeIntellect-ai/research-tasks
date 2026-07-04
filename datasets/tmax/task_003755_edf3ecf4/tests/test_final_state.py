# test_final_state.py
import os
import subprocess
import glob
import threading
import time
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

def test_detector_adversarial_corpus():
    """Test the standalone detector against the adversarial corpus."""
    detector_path = "/home/user/detector"
    assert os.path.exists(detector_path), f"Detector not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable"

    evil_files = glob.glob("/app/corpus/evil/*.json")
    clean_files = glob.glob("/app/corpus/clean/*.json")

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for filepath in evil_files:
        result = subprocess.run([detector_path, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(filepath))

    clean_modified = []
    for filepath in clean_files:
        result = subprocess.run([detector_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(filepath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)

class DummyBackendHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass # Suppress logging

def test_reverse_proxy_filtering():
    """Test the reverse proxy filtering logic with live traffic."""
    # Start dummy backend on 9090
    server = HTTPServer(('127.0.0.1', 9090), DummyBackendHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    time.sleep(1) # Give the server a moment to start

    evil_payloads = [
        b'{"a": {"b": {"c": {"d": {"execute": "something"}}}}}',
        b'{"query": "SELECT * FROM users; DROP TABLE admin;"}',
        b'{"nested": {"test": "drop table users"}}'
    ]

    clean_payloads = [
        b'{"execute": "safe"}',
        b'{"a": {"b": {"c": {"execute": "safe"}}}}',
        b'{"query": "SELECT * FROM users;"}',
        b'{"message": "Please drop the table at the restaurant"}'
    ]

    evil_bypassed = 0
    for i, payload in enumerate(evil_payloads):
        req = urllib.request.Request("http://127.0.0.1:8080", data=payload, method="POST")
        req.add_header('Content-Type', 'application/json')
        try:
            urllib.request.urlopen(req, timeout=2)
            evil_bypassed += 1
        except urllib.error.HTTPError as e:
            assert e.code == 403, f"Evil payload {i} got HTTP {e.code} instead of 403"
        except urllib.error.URLError as e:
            pytest.fail(f"Proxy not reachable or connection error: {e}")

    clean_blocked = 0
    for i, payload in enumerate(clean_payloads):
        req = urllib.request.Request("http://127.0.0.1:8080", data=payload, method="POST")
        req.add_header('Content-Type', 'application/json')
        try:
            resp = urllib.request.urlopen(req, timeout=2)
            assert resp.getcode() == 200, f"Clean payload {i} got HTTP {resp.getcode()} instead of 200"
        except urllib.error.HTTPError as e:
            clean_blocked += 1
        except urllib.error.URLError as e:
            pytest.fail(f"Proxy not reachable or connection error: {e}")

    server.shutdown()
    server.server_close()

    assert evil_bypassed == 0, f"{evil_bypassed} of {len(evil_payloads)} evil payloads bypassed the proxy"
    assert clean_blocked == 0, f"{clean_blocked} of {len(clean_payloads)} clean payloads were blocked by the proxy"