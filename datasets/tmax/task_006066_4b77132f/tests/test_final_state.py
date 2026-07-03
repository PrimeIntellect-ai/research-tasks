# test_final_state.py
import os
import subprocess
import threading
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

def test_rust_verifier_compiled_and_works():
    binary_path = "/home/user/artifact_cache/verifier/target/debug/verifier"
    assert os.path.isfile(binary_path), f"Rust verifier binary not found at {binary_path}. Did you compile it?"

    # Check valid artifact
    proc_valid = subprocess.run([binary_path, "core-test"], capture_output=True)
    assert proc_valid.returncode == 0, "Verifier should exit with 0 for 'core-test'"

    # Check invalid artifact
    proc_invalid = subprocess.run([binary_path, "malicious"], capture_output=True)
    assert proc_invalid.returncode != 0, "Verifier should exit with non-zero for 'malicious'"

def test_test_results_log_exists_and_passed():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Test results log not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "2 passed" in content or "passed" in content, "The test results log does not indicate that tests passed."

def test_proxy_behavior():
    # To test the proxy we can import it and run it, and also run a dummy backend
    import sys
    sys.path.insert(0, "/home/user/artifact_cache")

    try:
        from proxy import ProxyHandler
    except ImportError:
        assert False, "Could not import ProxyHandler from proxy.py"

    # Start dummy backend
    class BackendHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="/home/user/artifact_cache/backend_storage", **kwargs)

    backend_server = HTTPServer(('localhost', 8081), BackendHandler)
    backend_thread = threading.Thread(target=backend_server.serve_forever)
    backend_thread.daemon = True
    backend_thread.start()

    # Start proxy server
    proxy_server = HTTPServer(('localhost', 8080), ProxyHandler)
    proxy_thread = threading.Thread(target=proxy_server.serve_forever)
    proxy_thread.daemon = True
    proxy_thread.start()

    time.sleep(0.5)

    try:
        # Test valid
        req = urllib.request.Request("http://localhost:8080/download/core-linux.tar.gz")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, "Valid artifact should return 200"
            data = response.read().decode('utf-8').strip()
            assert data == "dummy-data", f"Expected 'dummy-data', got {data}"

        # Test invalid
        req_invalid = urllib.request.Request("http://localhost:8080/download/malicious.sh")
        try:
            urllib.request.urlopen(req_invalid)
            assert False, "Invalid artifact should have raised an HTTPError"
        except urllib.error.HTTPError as e:
            assert e.code == 403, f"Expected 403 Forbidden, got {e.code}"
            err_data = e.read().decode('utf-8')
            assert "Invalid artifact" in err_data, "Expected 'Invalid artifact' in response body"
    finally:
        proxy_server.shutdown()
        proxy_server.server_close()
        backend_server.shutdown()
        backend_server.server_close()