# test_final_state.py

import os
import json
import time
import subprocess
import urllib.request
import urllib.error
import ssl
import pytest

PROVISION_SCRIPT = "/home/user/provision.py"
GATEWAY_SCRIPT = "/home/user/gateway.py"
SSL_CERT = "/home/user/ssl/cert.pem"
SSL_KEY = "/home/user/ssl/key.pem"
METRICS_FILE = "/home/user/web/metrics.json"

def test_provision_script_exists():
    assert os.path.exists(PROVISION_SCRIPT), f"{PROVISION_SCRIPT} does not exist."
    assert os.path.isfile(PROVISION_SCRIPT), f"{PROVISION_SCRIPT} is not a file."

def test_run_provision_script():
    # Run the provision script
    result = subprocess.run(["python3", PROVISION_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"provision.py failed to execute. stderr: {result.stderr}"

def test_ssl_certificates_generated():
    assert os.path.exists(SSL_CERT), f"SSL certificate {SSL_CERT} was not generated."
    assert os.path.exists(SSL_KEY), f"SSL key {SSL_KEY} was not generated."

def test_metrics_json_content():
    assert os.path.exists(METRICS_FILE), f"Metrics file {METRICS_FILE} was not generated."

    with open(METRICS_FILE, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{METRICS_FILE} does not contain valid JSON.")

    assert "vm" in metrics, "Key 'vm' missing in metrics.json"
    assert metrics["vm"] == "production-db-01", f"Expected vm 'production-db-01', got {metrics['vm']}"

    assert "vnc_port" in metrics, "Key 'vnc_port' missing in metrics.json"
    assert metrics["vnc_port"] == 5912, f"Expected vnc_port 5912, got {metrics['vnc_port']}"

    assert "status" in metrics, "Key 'status' missing in metrics.json"
    assert metrics["status"] == "running", f"Expected status 'running', got {metrics['status']}"

def test_gateway_server():
    assert os.path.exists(GATEWAY_SCRIPT), f"{GATEWAY_SCRIPT} was not generated."

    # Start the gateway server
    server_process = subprocess.Popen(["python3", GATEWAY_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Give the server a moment to start
        time.sleep(2)

        # Check if process is still running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            pytest.fail(f"gateway.py exited prematurely. stderr: {stderr.decode('utf-8')}")

        # Create an unverified SSL context to bypass self-signed cert errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = "https://127.0.0.1:8443/metrics.json"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                data = response.read().decode('utf-8')

                try:
                    metrics = json.loads(data)
                except json.JSONDecodeError:
                    pytest.fail("Response from gateway is not valid JSON.")

                assert metrics.get("vm") == "production-db-01", "Gateway response missing or incorrect 'vm' key."
                assert metrics.get("vnc_port") == 5912, "Gateway response missing or incorrect 'vnc_port' key."

        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to gateway server: {e}")

    finally:
        # Terminate the server
        server_process.terminate()
        server_process.wait(timeout=5)