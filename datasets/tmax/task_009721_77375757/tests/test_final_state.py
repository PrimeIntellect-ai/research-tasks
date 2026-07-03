# test_final_state.py

import os
import re
import time
import subprocess
import urllib.request
import urllib.error
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def test_haproxy_config_and_process():
    """Verify HAProxy configuration and process."""
    cfg_path = "/home/user/haproxy.cfg"
    assert os.path.exists(cfg_path), f"HAProxy config {cfg_path} does not exist."

    with open(cfg_path, 'r') as f:
        content = f.read()

    # Check frontend and backend
    assert "app_front" in content, "Frontend 'app_front' not found in config."
    assert "8080" in content, "Port 8080 not found in config."
    assert "mock_pool" in content, "Backend 'mock_pool' not found in config."
    assert "roundrobin" in content.lower(), "Round-robin load balancing not found in config."

    # Check servers
    assert re.search(r"server\s+mock1\s+(127\.0\.0\.1|localhost):8081", content), "mock1 server not configured correctly."
    assert re.search(r"server\s+mock2\s+(127\.0\.0\.1|localhost):8082", content), "mock2 server not configured correctly."
    assert re.search(r"server\s+mock3\s+(127\.0\.0\.1|localhost):8083", content), "mock3 server not configured correctly."

    # Check backup server
    assert re.search(r"server\s+cloud_api\s+(127\.0\.0\.1|localhost):8084.*\bbackup\b", content), "cloud_api backup server not configured correctly."

    # Check process
    try:
        output = subprocess.check_output(["pgrep", "-f", "haproxy.*-f /home/user/haproxy.cfg"]).decode()
        assert output.strip(), "HAProxy is not running with the specified config."
    except subprocess.CalledProcessError:
        pytest.fail("HAProxy process is not running with the specified config.")

def test_port_forwarder():
    """Verify the port forwarder script and process."""
    script_path = "/home/user/forwarder.sh"
    assert os.path.exists(script_path), f"Forwarder script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Forwarder script {script_path} is not executable."

    try:
        # Check if socat is running with 9000 and 8080
        output = subprocess.check_output(["pgrep", "-f", "socat.*9000.*8080"]).decode()
        assert output.strip(), "socat is not forwarding from 9000 to 8080."
    except subprocess.CalledProcessError:
        try:
            # Check if forwarder.sh is running
            output = subprocess.check_output(["pgrep", "-f", "forwarder.sh"]).decode()
            assert output.strip(), "forwarder.sh is not running and socat is not found."
        except subprocess.CalledProcessError:
            pytest.fail("Neither socat nor forwarder.sh is running.")

def test_cost_optimizer():
    """Verify the cost optimizer script functionality."""
    script_path = "/home/user/cost_optimizer.sh"
    assert os.path.exists(script_path), f"Cost optimizer script {script_path} does not exist."

    try:
        output = subprocess.check_output(["pgrep", "-f", "cost_optimizer.sh"]).decode()
        assert output.strip(), "cost_optimizer.sh is not running in the background."
    except subprocess.CalledProcessError:
        pytest.fail("cost_optimizer.sh is not running in the background.")

    # Trigger the optimizer
    usage_path = "/home/user/usage.txt"
    log_path = "/home/user/scaling.log"

    with open(usage_path, "w") as f:
        f.write("STATUS=IDLE\n")

    # Wait for the script to process (2 seconds sleep + buffer)
    time.sleep(3.5)

    assert os.path.exists(log_path), f"Scaling log {log_path} was not created."
    with open(log_path, "r") as f:
        log_content = f.read()

    assert "FinOps: Scaled down mock3" in log_content, "Cost optimizer failed to log the correct scaling action."

class MockServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.server.server_port == 8081:
            self.wfile.write(b"MOCK1")
        elif self.server.server_port == 8084:
            self.wfile.write(b"CLOUD")
        else:
            self.wfile.write(b"OTHER")

    def log_message(self, format, *args):
        pass

def run_mock_server(port):
    server = HTTPServer(('127.0.0.1', port), MockServerHandler)
    server.serve_forever()

def test_network_integration():
    """Verify that traffic to 9000 is correctly routed to the mock servers."""
    # Start dummy servers
    t1 = threading.Thread(target=run_mock_server, args=(8081,), daemon=True)
    t4 = threading.Thread(target=run_mock_server, args=(8084,), daemon=True)
    t1.start()
    t4.start()

    # Give servers a moment to start
    time.sleep(1)

    try:
        req = urllib.request.Request("http://127.0.0.1:9000")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode()
            assert body in ["MOCK1", "CLOUD"], f"Unexpected response from routing: {body}"
    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")