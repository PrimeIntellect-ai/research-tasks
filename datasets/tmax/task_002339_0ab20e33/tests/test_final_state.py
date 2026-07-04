# test_final_state.py

import os
import json
import urllib.request
from urllib.error import HTTPError, URLError
import pytest

def get_parity(filename, size):
    ascii_sum = sum(ord(c) for c in filename)
    return (size ^ ascii_sum) % 251

def test_script_exists():
    script_path = "/home/user/workspace/verify_and_route.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_nginx_conf_exists():
    conf_path = "/home/user/workspace/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx configuration {conf_path} does not exist."

def test_python_backend_running():
    url = "http://127.0.0.1:9000/build_alpha.tar"
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected Python backend to return 200 for {url}, got {response.status}"
    except HTTPError as e:
        pytest.fail(f"Python backend returned HTTP error {e.code} for {url}")
    except URLError as e:
        pytest.fail(f"Could not connect to Python backend on port 9000: {e.reason}")

def test_nginx_routing():
    manifest_path = "/home/user/workspace/artifacts/manifest.json"
    assert os.path.isfile(manifest_path), "Manifest file missing."

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    for item in manifest.get("artifacts", []):
        filename = item["filename"]
        expected_parity = item["expected_parity"]
        filepath = f"/home/user/workspace/artifacts/{filename}"

        if not os.path.isfile(filepath):
            continue

        actual_size = os.path.getsize(filepath)
        actual_parity = get_parity(filename, actual_size)

        url = f"http://127.0.0.1:8080/download/{filename}"
        req = urllib.request.Request(url, method="HEAD")

        if actual_parity == expected_parity:
            # Should be valid -> 200 OK
            try:
                with urllib.request.urlopen(req, timeout=2) as response:
                    assert response.status == 200, f"Expected 200 OK for valid artifact {filename}, got {response.status}"
            except HTTPError as e:
                pytest.fail(f"Expected 200 OK for valid artifact {filename}, but got HTTP {e.code}")
            except URLError as e:
                pytest.fail(f"Could not connect to Nginx on port 8080: {e.reason}")
        else:
            # Should be invalid -> 403 Forbidden
            try:
                with urllib.request.urlopen(req, timeout=2) as response:
                    pytest.fail(f"Expected 403 Forbidden for corrupted artifact {filename}, but got {response.status}")
            except HTTPError as e:
                assert e.code == 403, f"Expected 403 Forbidden for corrupted artifact {filename}, but got HTTP {e.code}"
            except URLError as e:
                pytest.fail(f"Could not connect to Nginx on port 8080: {e.reason}")