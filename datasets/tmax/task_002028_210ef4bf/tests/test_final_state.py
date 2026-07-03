# test_final_state.py
import os
import requests
import pytest

def test_rust_project_exists():
    assert os.path.isdir("/home/user/forensics_api"), "Rust project directory /home/user/forensics_api does not exist."

def test_api_unauthorized():
    url = "http://127.0.0.1:8181/recovered-data"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for unauthorized request, got {response.status_code}"

def test_api_authorized_and_redacted():
    url = "http://127.0.0.1:8181/recovered-data"
    headers = {"Authorization": "Bearer forensics-auth-token"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for authorized request, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    assert isinstance(data, list), "Expected response JSON to be a list"
    assert len(data) == 2, f"Expected 2 items in the response list, got {len(data)}"

    expected_data = [
        {
            "id": 1,
            "username": "admin",
            "ssn": "REDACTED_SSN",
            "private_ssh_key": "REDACTED_KEY"
        },
        {
            "id": 2,
            "username": "dev",
            "ssn": "REDACTED_SSN",
            "private_ssh_key": "REDACTED_KEY"
        }
    ]

    for item in expected_data:
        assert item in data, f"Expected item {item} not found in response data"