# test_final_state.py
import os
import requests
import pytest

PORT = 8282
TOKEN = "TRITON-77X-912"
URL = f"http://127.0.0.1:{PORT}/api/v1/process"

def test_libsorter_built():
    assert os.path.isfile("/home/user/clib/libsorter.so"), "libsorter.so was not built in /home/user/clib/"

def test_server_unauthorized():
    try:
        response = requests.post(URL, json={"arrays": [[1, 2], [3, 4]]}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {response.status_code}"

def test_server_authorized_process():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"arrays": [[10, 2, 8], [1, 9]]}
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Got: {data}"
    assert data["result"] == [1, 2, 8, 9, 10], f"Expected result [1, 2, 8, 9, 10], got {data['result']}"