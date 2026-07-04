# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_nginx_proxy_returns_correct_build_order():
    url = "http://127.0.0.1:9000/api/v1/build_order"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

            data = response.read().decode('utf-8')
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                pytest.fail(f"Response from {url} is not valid JSON: {data}")

            expected_order = ["D", "B", "E", "C", "A"]
            assert parsed_data == expected_order, f"Expected build order {expected_order}, but got {parsed_data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {url}: {e}")

def test_api_server_returns_correct_build_order():
    url = "http://127.0.0.1:8080/build_order"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

            data = response.read().decode('utf-8')
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                pytest.fail(f"Response from {url} is not valid JSON: {data}")

            expected_order = ["D", "B", "E", "C", "A"]
            assert parsed_data == expected_order, f"Expected build order {expected_order}, but got {parsed_data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API server at {url}: {e}")

def test_nginx_config_exists():
    config_path = "/home/user/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx configuration file missing at {config_path}"