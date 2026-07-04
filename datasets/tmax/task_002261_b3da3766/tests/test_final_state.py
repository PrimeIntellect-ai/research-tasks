# test_final_state.py
import os
import requests

def test_shared_library_exists():
    assert os.path.exists('/app/libecc.so'), "/app/libecc.so does not exist. Did you compile the C library?"

def test_api_unauthorized():
    url = "http://127.0.0.1:9090/process"
    headers = {
        "Authorization": "Bearer WRONGTOKEN",
        "Content-Type": "application/json"
    }
    payload = {"data": "test"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to the API at {url}: {e}"

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for wrong token, got {response.status_code}"

def test_api_authorized_and_processing():
    url = "http://127.0.0.1:9090/process"
    headers = {
        "Authorization": "Bearer AUTH-77X9Q2",
        "Content-Type": "application/json"
    }
    payload = {"data": "hello world"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to the API at {url}: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK for correct token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Expected JSON response, got: {response.text}"

    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
    assert data.get("checksum") == 3501256372, f"Expected checksum 3501256372 for 'hello world', got {data.get('checksum')}"