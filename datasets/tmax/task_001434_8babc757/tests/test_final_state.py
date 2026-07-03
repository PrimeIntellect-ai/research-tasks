# test_final_state.py

import pytest
import requests

URL = "http://127.0.0.1:8080/predict"
VALID_TOKEN = "Bearer etl-pipeline-secret-2024"

def test_auth_missing_token():
    """Test that missing token returns 401."""
    payload = {"sensor_id": 1, "v1": 0.0, "v2": 0.0, "v3": 0.0}
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

def test_auth_invalid_token():
    """Test that invalid token returns 401."""
    payload = {"sensor_id": 1, "v1": 0.0, "v2": 0.0, "v3": 0.0}
    headers = {"Authorization": "Bearer wrong-token"}
    response = requests.post(URL, json=payload, headers=headers, timeout=5)

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}"

def test_predict_anomaly_true():
    """Test anomaly detection for a true anomaly."""
    # (v1 + v2) > 15.0 AND v3 < 2.0 -> Anomaly
    payload = {"sensor_id": 42, "v1": 10.5, "v2": 6.1, "v3": 1.2}
    headers = {"Authorization": VALID_TOKEN}
    response = requests.post(URL, json=payload, headers=headers, timeout=5)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    data = response.json()
    assert "anomaly" in data, "Response JSON missing 'anomaly' key"
    assert data["anomaly"] is True, f"Expected anomaly=True for payload {payload}, got {data['anomaly']}"

def test_predict_anomaly_false():
    """Test anomaly detection for a normal reading."""
    # (v1 + v2) <= 15.0 OR v3 >= 2.0 -> Not Anomaly
    payload = {"sensor_id": 42, "v1": 5.0, "v2": 5.0, "v3": 5.0}
    headers = {"Authorization": VALID_TOKEN}
    response = requests.post(URL, json=payload, headers=headers, timeout=5)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    data = response.json()
    assert "anomaly" in data, "Response JSON missing 'anomaly' key"
    assert data["anomaly"] is False, f"Expected anomaly=False for payload {payload}, got {data['anomaly']}"

def test_predict_edge_cases():
    """Test anomaly detection near the decision boundaries."""
    headers = {"Authorization": VALID_TOKEN}

    # Case 1: v1+v2 > 15.0 but v3 >= 2.0 -> False
    payload1 = {"sensor_id": 10, "v1": 10.0, "v2": 6.0, "v3": 2.5}
    resp1 = requests.post(URL, json=payload1, headers=headers, timeout=5)
    assert resp1.json().get("anomaly") is False, f"Expected False for {payload1}"

    # Case 2: v1+v2 <= 15.0 and v3 < 2.0 -> False
    payload2 = {"sensor_id": 11, "v1": 7.0, "v2": 7.0, "v3": 1.0}
    resp2 = requests.post(URL, json=payload2, headers=headers, timeout=5)
    assert resp2.json().get("anomaly") is False, f"Expected False for {payload2}"

    # Case 3: v1+v2 > 15.0 and v3 < 2.0 -> True
    payload3 = {"sensor_id": 12, "v1": 8.0, "v2": 7.5, "v3": 1.9}
    resp3 = requests.post(URL, json=payload3, headers=headers, timeout=5)
    assert resp3.json().get("anomaly") is True, f"Expected True for {payload3}"