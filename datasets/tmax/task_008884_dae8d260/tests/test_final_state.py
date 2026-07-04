# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def test_sanitizer_fixed():
    path = "/home/user/waf-proxy/sanitizer.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    assert "max_len" in content, "sanitizer.c does not seem to use max_len to prevent buffer overflow."

def test_build_script_exists():
    path = "/home/user/waf-proxy/build.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_run_script_exists():
    path = "/home/user/waf-proxy/run.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_statically_linked_binary():
    binary_path = "/home/user/waf-proxy/static-waf"
    assert os.path.isfile(binary_path), f"Binary {binary_path} was not built."

    # Check if statically linked using ldd or file
    try:
        output = subprocess.check_output(["ldd", binary_path], stderr=subprocess.STDOUT).decode('utf-8')
        assert "not a dynamic executable" in output, "Binary is not statically linked (ldd output indicates dynamic dependencies)."
    except subprocess.CalledProcessError as e:
        # ldd returns non-zero for statically linked binaries on some systems
        output = e.output.decode('utf-8')
        assert "not a dynamic executable" in output, "Binary is not statically linked."

def test_proxy_running_and_pid_file():
    pid_file = "/home/user/waf-proxy/proxy.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "PID file does not contain a valid numeric PID."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

class MockBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        user = self.headers.get("X-Custom-User", "")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(user.encode('utf-8'))

    def log_message(self, format, *args):
        pass

def test_proxy_truncation_behavior():
    # Start mock backend on 9090
    server = HTTPServer(("127.0.0.1", 9090), MockBackendHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    time.sleep(1) # Give server time to start

    try:
        # Test normal request
        req = urllib.request.Request("http://127.0.0.1:8080/")
        req.add_header("X-Custom-User", "alice")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                body = response.read().decode('utf-8')
                assert body == "alice", f"Expected 'alice', got '{body}'"
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to proxy or proxy returned error: {e}")

        # Test overflow request
        overflow_payload = "A" * 100
        expected_trunc = "A" * 63

        req = urllib.request.Request("http://127.0.0.1:8080/")
        req.add_header("X-Custom-User", overflow_payload)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                body = response.read().decode('utf-8')
                assert body == expected_trunc, f"Expected truncated payload of length 63, got length {len(body)}"
        except urllib.error.URLError as e:
            pytest.fail(f"Proxy crashed or returned error on long header: {e}")

    finally:
        server.shutdown()
        server.server_close()
        thread.join()