# test_final_state.py

import os
import requests
import pytest

def test_test_analyzer_exists():
    assert os.path.isfile("/app/test_analyzer.py"), "Regression test /app/test_analyzer.py was not created."

def test_http_server_unauthorized():
    url = "http://127.0.0.1:8000/anomalies"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    response = requests.get(url, headers=headers, timeout=2)
    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong token, got {response.status_code}"

def test_http_server_authorized():
    url = "http://127.0.0.1:8000/anomalies"
    headers = {"Authorization": "Bearer SCARLET-MACAW-77"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for correct token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "anomalous_ips" in data, "JSON response missing 'anomalous_ips' key."
    expected_ips = ["10.0.0.99", "192.168.1.105"]
    assert sorted(data["anomalous_ips"]) == expected_ips, f"Expected anomalous IPs {expected_ips}, got {data['anomalous_ips']}"