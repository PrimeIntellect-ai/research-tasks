# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import ssl
import subprocess
import time

def test_files_created():
    expected_files = [
        "/home/user/exporter.py",
        "/home/user/cert.pem",
        "/home/user/key.pem",
        "/home/user/supervisord.conf"
    ]
    for filepath in expected_files:
        assert os.path.exists(filepath), f"Expected file {filepath} is missing."

def test_supervisord_config():
    conf_path = "/home/user/supervisord.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()

    assert "autorestart=true" in content.replace(" ", ""), "supervisord.conf must contain autorestart=true"
    assert "exporter.py" in content, "supervisord.conf must execute exporter.py"
    assert "exporter.log" in content, "supervisord.conf must route logs to exporter.log"

def test_processes_running():
    # Check if supervisord is running with the correct config
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisord.*/home/user/supervisord.conf"]).decode()
        assert output.strip(), "supervisord is not running with /home/user/supervisord.conf"
    except subprocess.CalledProcessError:
        assert False, "supervisord process not found"

    # Check if exporter.py is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "exporter.py"]).decode()
        assert output.strip(), "exporter.py is not running"
    except subprocess.CalledProcessError:
        assert False, "exporter.py process not found"

def test_https_server_response():
    # Allow some time for the server to start if it was just spawned
    time.sleep(1)

    url = "https://127.0.0.1:8443"

    # Create an unverified SSL context to bypass self-signed cert errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            status_code = response.getcode()
            assert status_code == 200, f"Expected HTTP 200, got {status_code}"

            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

            body = response.read().decode("utf-8")
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                assert False, f"Response body is not valid JSON: {body}"

            expected_data = {"cpu": 50, "mem": 1024}
            assert data == expected_data, f"Expected JSON payload {expected_data}, got {data}"

    except urllib.error.URLError as e:
        assert False, f"Failed to connect to {url}: {e}"