# test_final_state.py

import os
import stat
import requests
import pytest
import re

def test_legacy_logs_permissions():
    log_dir = "/home/user/legacy_logs"
    assert os.path.exists(log_dir), f"Directory {log_dir} does not exist."
    st = os.stat(log_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions of {log_dir} are {oct(perms)}, expected 0o700."

def test_logrotate_config():
    config_path = "/home/user/logrotate.conf"
    assert os.path.exists(config_path), f"Logrotate config {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "/home/user/legacy_logs/node.log" in content, "Logrotate config missing target log file."
    assert re.search(r'\bdaily\b', content), "Logrotate config missing 'daily' directive."
    assert re.search(r'\brotate\s+7\b', content), "Logrotate config missing 'rotate 7' directive."
    assert re.search(r'\bcompress\b', content), "Logrotate config missing 'compress' directive."

def test_systemd_units_exist():
    systemd_dir = "/home/user/.config/systemd/user"
    legacy_node_svc = os.path.join(systemd_dir, "legacy-node.service")
    legacy_bridge_svc = os.path.join(systemd_dir, "legacy-bridge.service")

    assert os.path.exists(legacy_node_svc), f"Systemd unit {legacy_node_svc} does not exist."
    assert os.path.exists(legacy_bridge_svc), f"Systemd unit {legacy_bridge_svc} does not exist."

def test_http_bridge_unauthorized():
    url = "http://127.0.0.1:8080/status"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to bridge service at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized, got {response.status_code}."

def test_http_bridge_authorized():
    url = "http://127.0.0.1:8080/status"
    headers = {"Authorization": "Bearer cloud-migration-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to bridge service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."
    assert "DATA_NODE_OK_V9" in response.text, f"Expected 'DATA_NODE_OK_V9' in response body, got {response.text!r}."