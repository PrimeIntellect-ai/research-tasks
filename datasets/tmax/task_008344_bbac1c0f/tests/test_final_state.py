# test_final_state.py
import os
import json
import urllib.request
import pytest

def test_libsecret_so_exists():
    path = "/home/user/legacy/libsecret.so"
    assert os.path.isfile(path), f"Shared library {path} was not created"

def test_final_output_json():
    path = "/home/user/final_output.json"
    assert os.path.isfile(path), f"Output file {path} does not exist"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON")

    assert data.get("status") == "success", f"Expected 'status' to be 'success' in {path}"
    assert data.get("data") == "API_KEY_998877", f"Expected 'data' to be 'API_KEY_998877' in {path}"

def test_api_service_running():
    url = "http://127.0.0.1:8080/secret"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"API service at {url} did not return 200 OK"
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"API service did not set Content-Type: application/json (got {content_type})"

            data = json.loads(response.read().decode("utf-8"))
            assert data.get("status") == "success", "API service JSON response status mismatch"
            assert data.get("data") == "API_KEY_998877", "API service JSON response data mismatch"
    except Exception as e:
        pytest.fail(f"Failed to connect to API service on 8080 or invalid response: {e}")

def test_proxy_service_running():
    url = "http://127.0.0.1:9090/secret"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Proxy service at {url} did not return 200 OK"

            # Check custom header
            headers = {k.lower(): v for k, v in response.getheaders()}
            assert headers.get("x-proxy-routed", "").lower() == "true", "Proxy did not inject 'X-Proxy-Routed: true' header"

            # Check content
            data = json.loads(response.read().decode("utf-8"))
            assert data.get("status") == "success", "Proxy service JSON response status mismatch"
            assert data.get("data") == "API_KEY_998877", "Proxy service JSON response data mismatch"
    except Exception as e:
        pytest.fail(f"Failed to connect to Proxy service on 9090 or invalid response: {e}")