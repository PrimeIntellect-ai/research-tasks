# test_final_state.py
import pytest
import requests

def test_service_record_1():
    url = "http://127.0.0.1:8888/record/1"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for record 1, got {response.status_code}"
    assert response.text.strip() == "SYSTEM_STARTUP", f"Expected 'SYSTEM_STARTUP', got '{response.text}'"

def test_service_record_2():
    url = "http://127.0.0.1:8888/record/2"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for record 2, got {response.status_code}"
    assert response.text.strip() == "USER_LOGIN_SUCCESS", f"Expected 'USER_LOGIN_SUCCESS', got '{response.text}'"

def test_service_record_3_skipped():
    url = "http://127.0.0.1:8888/record/3"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 404, f"Expected status 404 for corrupted record 3, got {response.status_code}"

def test_service_record_4():
    url = "http://127.0.0.1:8888/record/4"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for record 4, got {response.status_code}"
    assert response.text.strip() == "CRITICAL_SYSTEM_RECOVERED", f"Expected 'CRITICAL_SYSTEM_RECOVERED', got '{response.text}'"