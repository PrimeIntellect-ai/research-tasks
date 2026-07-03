# test_final_state.py
import os
import subprocess
import time
import urllib.request
import urllib.error
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

class DummyBackendHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass

@pytest.fixture(scope="module")
def backend_server():
    server = HTTPServer(('127.0.0.1', 9000), DummyBackendHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()

@pytest.fixture(scope="module")
def proxy_process():
    proxy_path = "/home/user/proxy"
    assert os.path.exists(proxy_path), f"Proxy executable not found at {proxy_path}"
    assert os.access(proxy_path, os.X_OK), f"Proxy at {proxy_path} is not executable"

    proc = subprocess.Popen([proxy_path])
    time.sleep(2) # Wait for proxy to start

    # Check if process is still running
    if proc.poll() is not None:
        pytest.fail(f"Proxy process exited prematurely with code {proc.returncode}")

    yield proc
    proc.terminate()
    proc.wait()

def test_proxy_behavior(backend_server, proxy_process):
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    clean_modified = []
    evil_bypassed = []

    for fpath in clean_files:
        with open(fpath, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://127.0.0.1:8080", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status != 200:
                    clean_modified.append(os.path.basename(fpath))
        except urllib.error.HTTPError as e:
            clean_modified.append(f"{os.path.basename(fpath)} (HTTP {e.code})")
        except Exception as e:
            clean_modified.append(f"{os.path.basename(fpath)} ({type(e).__name__})")

    for fpath in evil_files:
        with open(fpath, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://127.0.0.1:8080", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status != 403:
                    evil_bypassed.append(f"{os.path.basename(fpath)} (HTTP {response.status})")
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_bypassed.append(f"{os.path.basename(fpath)} (HTTP {e.code})")
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(fpath)} ({type(e).__name__})")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)