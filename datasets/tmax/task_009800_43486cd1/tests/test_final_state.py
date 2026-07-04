# test_final_state.py
import os
import json
import ssl
import urllib.request
import urllib.error

def test_tls_certs_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

def test_https_server_health_endpoint():
    url = "https://127.0.0.1:8443/health"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8').strip()
            assert status == 200, f"Expected HTTP 200, got {status}"
            assert body == "OK", f"Expected response body 'OK', got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to {url}: {e}"

def test_mock_group_file_updated():
    path = "/home/user/app-groups.conf"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    web_admin_line = None
    for line in lines:
        if line.startswith("web-admin:"):
            web_admin_line = line
            break

    assert web_admin_line is not None, "Group 'web-admin' not found in app-groups.conf."

    parts = web_admin_line.split(":")
    assert len(parts) >= 4, "Invalid format for web-admin group line."

    users = [u.strip() for u in parts[3].split(",") if u.strip()]
    assert "deployer" in users, f"'deployer' not found in web-admin users list. Found: {users}"

def test_mock_firewall_file_updated():
    path = "/home/user/fw-rules.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    assert isinstance(data, list), f"Expected JSON array in {path}."

    expected_rule = {"port": 8443, "action": "allow"}
    assert expected_rule in data, f"Expected rule {expected_rule} not found in {path}."

def test_provision_log_updated():
    path = "/home/user/provision.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected_line = "Provisioning complete: server reachable"
    with open(path, "r") as f:
        content = f.read()

    assert expected_line in content, f"Expected line '{expected_line}' not found in {path}."