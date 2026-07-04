# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_build_sh_exists_and_executable():
    path = "/home/user/app/build.sh"
    assert os.path.isfile(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_test_result_txt():
    path = "/home/user/test_result.txt"
    assert os.path.isfile(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"{path} does not contain valid JSON")
    assert data.get("status") == "secure", f"{path} does not contain the correct status"

def test_status_endpoint_and_headers():
    url = "http://127.0.0.1:8080/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
            headers = response.headers
    except Exception as e:
        pytest.fail(f"Failed to access {url}: {e}")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Response from {url} is not valid JSON")

    assert data.get("status") == "secure", f"Response from {url} is incorrect: {data}"

    # Check for custom header
    header_val = headers.get("X-Security-Protection")
    assert header_val == "active", f"Expected X-Security-Protection: active, got {header_val}"

def test_ssrf_protection():
    url = "http://127.0.0.1:8080/fetch?url=http://127.0.0.1/admin"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to access {url}: {e}")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Response from {url} is not valid JSON")

    assert data.get("error") == "SSRF blocked", f"SSRF protection failed, got: {data}"