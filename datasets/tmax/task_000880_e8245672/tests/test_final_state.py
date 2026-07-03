# test_final_state.py

import os
import json
import re
import urllib.request
import ssl
import time

def test_directories_exist():
    assert os.path.isdir("/home/user/certs"), "Directory /home/user/certs does not exist."
    assert os.path.isdir("/home/user/edge_data"), "Directory /home/user/edge_data does not exist."

def test_certificates_exist():
    assert os.path.isfile("/home/user/certs/edge.crt"), "Certificate file /home/user/certs/edge.crt does not exist."
    assert os.path.isfile("/home/user/certs/edge.key"), "Key file /home/user/certs/edge.key does not exist."

def test_deploy_script_executable():
    assert os.path.isfile("/home/user/deploy.sh"), "Deploy script /home/user/deploy.sh does not exist."
    assert os.access("/home/user/deploy.sh", os.X_OK), "Deploy script /home/user/deploy.sh is not executable."

def test_config_json_content():
    config_path = "/home/user/edge_data/config.json"
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."
    with open(config_path, "r") as f:
        content = f.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {config_path} does not contain valid JSON.")

    assert data.get("device_id") == "Gateway-Alpha", "device_id in config.json is not 'Gateway-Alpha'."
    assert data.get("sensor") == "Humidity", "sensor in config.json is not 'Humidity'."

def test_run_log_content():
    log_path = "/home/user/run.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    assert re.search(r"^PYTHON_PID=\d+$", content, re.MULTILINE), "PYTHON_PID not found or invalid in run.log."
    assert re.search(r"^SOCAT_PID=\d+$", content, re.MULTILINE), "SOCAT_PID not found or invalid in run.log."

def test_tls_port_forwarding():
    # Allow a brief moment in case services are just coming up
    time.sleep(1)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://localhost:8443/config.json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
                assert data.get("device_id") == "Gateway-Alpha", "device_id fetched via TLS does not match."
                assert data.get("sensor") == "Humidity", "sensor fetched via TLS does not match."
            except json.JSONDecodeError:
                assert False, "Fetched content via TLS is not valid JSON."
    except Exception as e:
        assert False, f"Failed to fetch {url} via TLS: {e}"