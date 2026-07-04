# test_final_state.py

import os
import json
import subprocess
import pytest

def test_routes_json_exists_and_correct():
    json_path = "/home/user/routes.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_path} as JSON: {e}")

    expected_mapping = {
        "/api/v1/auth": "http://127.0.0.1:5001",
        "/api/v1/billing": "http://127.0.0.1:5002",
        "/api/v2/catalog": "http://127.0.0.1:5003"
    }

    assert data == expected_mapping, f"JSON content in {json_path} does not match expected mapping."

def test_nginx_conf_exists_and_valid():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."

    # Validate syntax using nginx -t
    cmd = ["nginx", "-t", "-c", conf_path, "-g", "pid /home/user/nginx.pid;"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Nginx configuration validation failed:\n{result.stderr}"

def test_nginx_conf_contents():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    # Check for required blocks and directives
    assert "events" in content, "Nginx config missing 'events' block."
    assert "http" in content, "Nginx config missing 'http' block."
    assert "9000" in content, "Nginx config missing port 9000 in server block."

    # Check for logs
    assert "/home/user/error.log" in content, "Nginx config missing error_log directive pointing to /home/user/error.log"
    assert "/home/user/access.log" in content, "Nginx config missing access_log directive pointing to /home/user/access.log"

    # Check for proxy_pass directives
    expected_proxy_passes = [
        "proxy_pass http://127.0.0.1:5001",
        "proxy_pass http://127.0.0.1:5002",
        "proxy_pass http://127.0.0.1:5003"
    ]

    for pp in expected_proxy_passes:
        assert pp in content, f"Nginx config missing expected directive: '{pp}'"