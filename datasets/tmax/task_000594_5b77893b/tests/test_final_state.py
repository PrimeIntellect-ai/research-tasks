# test_final_state.py

import os
import ssl
import urllib.request
import subprocess
import time

def test_compiled_server():
    server_path = "/home/user/server"
    assert os.path.isfile(server_path), f"Compiled executable {server_path} is missing."
    assert os.access(server_path, os.X_OK), f"File {server_path} is not executable."

def test_certificates():
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"
    assert os.path.isfile(cert_path), f"Certificate {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key {key_path} is missing."

    # Check CN = localhost
    cmd = ["openssl", "x509", "-in", cert_path, "-text", "-noout"]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to parse certificate with openssl: {e.output.decode()}"

    assert "CN = localhost" in output or "CN=localhost" in output, "Certificate does not have Common Name (CN) set to localhost."

def test_service_running_and_log():
    # Make a request to the socat TLS endpoint
    url = "https://127.0.0.1:8443"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            body = response.read().decode()
            assert body == "OK", f"Expected response 'OK', got '{body}'"
    except Exception as e:
        assert False, f"Failed to connect to HTTPS endpoint on port 8443: {e}"

    # Allow some time for the log to be flushed
    time.sleep(0.5)

    log_path = "/home/user/app.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "Connection received" in log_content, f"Log file {log_path} does not contain 'Connection received'."

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    # Clean up content to make parsing easier (remove comments, extra spaces)
    lines = [line.split('#')[0].strip() for line in content.splitlines()]
    text = " ".join(lines)

    assert "size 1k" in text or "size=1k" in text.replace(" ", ""), "Logrotate config missing 'size 1k'."
    assert "rotate 3" in text or "rotate=3" in text.replace(" ", ""), "Logrotate config missing 'rotate 3'."
    assert "compress" in text.split(), "Logrotate config missing 'compress'."
    assert "missingok" in text.split(), "Logrotate config missing 'missingok'."