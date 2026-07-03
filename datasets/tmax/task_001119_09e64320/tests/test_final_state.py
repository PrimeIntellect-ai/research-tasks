# test_final_state.py

import os
import requests
import pytest
import time

def test_libcore_a_exists():
    assert os.path.isfile("/home/user/project/clib/libcore.a"), "The static library libcore.a was not successfully built at /home/user/project/clib/libcore.a"

def test_server_binary_exists():
    assert os.path.isfile("/home/user/project/bin/server"), "The Go binary was not successfully built at /home/user/project/bin/server"

def test_server_running_and_unauthorized():
    url = "http://127.0.0.1:8443/ping"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running on the correct port? Error: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when missing token, but got {response.status_code}"

def test_server_running_and_authorized():
    url = "http://127.0.0.1:8443/ping"
    headers = {"Authorization": "Bearer AlphaBravo99"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running on the correct port? Error: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, but got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but got: {response.text}")

    assert data.get("status") == "ok", f"Expected response JSON {{'status': 'ok'}}, but got {data}"