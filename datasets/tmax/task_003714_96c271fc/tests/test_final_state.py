# test_final_state.py

import os
import requests
import time

def test_service_health_endpoint_success():
    """Verify that the service is running, listening on port 9090, and returns 200 OK with correct auth."""
    url = "http://127.0.0.1:9090/health"
    headers = {"Authorization": "Bearer Z77-K9-BETA"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service at {url}. Is it running on port 9090? Error: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
        assert data.get("status") == "ok", f"Expected response body to contain {{'status': 'ok'}}, got {data}"
    except ValueError:
        assert False, f"Expected JSON response, got: {response.text}"

def test_service_health_endpoint_unauthorized():
    """Verify that the service rejects requests without the correct auth token."""
    url = "http://127.0.0.1:9090/health"
    headers = {"Authorization": "Bearer WRONG-TOKEN"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service at {url}. Error: {e}"

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for bad token, got {response.status_code}."

def test_main_go_panic_removed():
    """Verify that the panic has been removed from main.go."""
    main_go_path = "/home/user/cache-service/main.go"
    assert os.path.isfile(main_go_path), f"The file {main_go_path} does not exist."

    with open(main_go_path, "r") as f:
        content = f.read()

    assert 'panic(' not in content, f"The panic statement is still present in {main_go_path}."