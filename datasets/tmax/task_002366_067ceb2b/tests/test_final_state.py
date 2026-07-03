# test_final_state.py

import os
import time
import socket
import tarfile
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def test_directories_exist():
    """Verify that the required directory structure exists."""
    dirs = [
        "/home/user/ci-system/commits",
        "/home/user/ci-system/workspace",
        "/home/user/ci-system/logs"
    ]
    for d in dirs:
        assert os.path.exists(d), f"Directory {d} does not exist."
        assert os.path.isdir(d), f"{d} is not a directory."

def test_binaries_exist_and_executable():
    """Verify that the Go binaries exist and are executable."""
    binaries = [
        "/home/user/egress_proxy",
        "/home/user/ci_runner"
    ]
    for b in binaries:
        assert os.path.exists(b), f"Binary {b} does not exist."
        assert os.access(b, os.X_OK), f"Binary {b} is not executable."

def test_proxy_listening():
    """Verify that the egress proxy is listening on 127.0.0.1:8080."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Port 8080 is not open. Egress proxy is not listening."
    finally:
        s.close()

class MockRegistryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SECRET_DATA")
    def log_message(self, format, *args):
        pass

def test_ci_runner_and_proxy_logic():
    """Verify the CI runner processing, proxy routing, and proxy blocking."""
    # Start mock registry on 9090
    server = HTTPServer(('127.0.0.1', 9090), MockRegistryHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    try:
        # Create a test job tarball
        job_name = "job-TEST"
        tar_path = f"/home/user/ci-system/commits/{job_name}.tar.gz"

        with tempfile.TemporaryDirectory() as tmpdir:
            ci_txt_path = os.path.join(tmpdir, "ci.txt")
            with open(ci_txt_path, "w") as f:
                f.write("sh test_script.sh\n")

            script_path = os.path.join(tmpdir, "test_script.sh")
            with open(script_path, "w") as f:
                f.write('echo "TEST" > test.out\n')
                f.write('curl -s http://allowed-registry.local/secret >> test.out\n')
                f.write('curl -s http://blocked.com/ >> test.out\n')

            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(ci_txt_path, arcname="ci.txt")
                tar.add(script_path, arcname="test_script.sh")

        # Wait for runner to process
        status_file = f"/home/user/ci-system/logs/{job_name}.status"
        pid_file = f"/home/user/ci-system/logs/{job_name}.pid"
        workspace_dir = f"/home/user/ci-system/workspace/{job_name}"
        out_file = f"{workspace_dir}/test.out"

        timeout = 15
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(status_file):
                break
            time.sleep(0.5)

        assert os.path.exists(status_file), f"Status file {status_file} was not created within {timeout} seconds."

        with open(status_file, "r") as f:
            status = f.read().strip()
        assert status == "SUCCESS", f"Expected status SUCCESS, got {status}"

        assert os.path.exists(pid_file), f"PID file {pid_file} was not created."
        with open(pid_file, "r") as f:
            pid_str = f.read().strip()
        assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"

        assert not os.path.exists(tar_path), f"Tarball {tar_path} was not deleted after processing."

        assert os.path.exists(out_file), f"Output file {out_file} was not created in workspace."
        with open(out_file, "r") as f:
            output = f.read()

        assert "TEST" in output, "Output file missing 'TEST'."
        assert "SECRET_DATA" in output, "Output file missing 'SECRET_DATA' from allowed registry."
        assert "BLOCKED" in output, "Output file missing 'BLOCKED' from blocked domain."

    finally:
        server.shutdown()
        server.server_close()