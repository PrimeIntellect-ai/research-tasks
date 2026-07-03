# test_final_state.py
import pytest
import requests

def test_api_job_a100():
    url = "http://127.0.0.1:8080/?job=A100"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or retrieve data for job A100: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower(), f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    expected_data = {
        "job_id": "A100",
        "hostname": "db-prod-eu",
        "expected_gb": 500,
        "actual_gb": 490,
        "status": "SUCCESS"
    }

    assert data == expected_data, f"Expected JSON response {expected_data}, got {data}"

def test_api_job_b200():
    url = "http://127.0.0.1:8080/?job=B200"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or retrieve data for job B200: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower(), f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    expected_data = {
        "job_id": "B200",
        "hostname": "db-prod-us",
        "expected_gb": 850,
        "actual_gb": 845,
        "status": "SUCCESS"
    }

    assert data == expected_data, f"Expected JSON response {expected_data}, got {data}"