# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
HEADERS = {"Authorization": "Bearer ml-data-token-992"}

def test_unauthorized_access():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph-distance", timeout=5)
        assert response.status_code in [401, 403], f"Expected 401 or 403 for unauthorized access, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:9090")

def test_graph_distance():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/graph-distance", headers=HEADERS, timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        data = response.json()
        assert "distance" in data, "Key 'distance' not found in response"
        assert data["distance"] == 2, f"Expected distance 2, got {data['distance']}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:9090")

def test_frequencies():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/frequencies", headers=HEADERS, timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        data = response.json()
        for key in ["A", "B", "C"]:
            assert key in data, f"Key '{key}' not found in response"
        assert abs(data["A"] - 2.0) < 0.1, f"Expected frequency A ~ 2.0, got {data['A']}"
        assert abs(data["B"] - 3.0) < 0.1, f"Expected frequency B ~ 3.0, got {data['B']}"
        assert abs(data["C"] - 1.0) < 0.1, f"Expected frequency C ~ 1.0, got {data['C']}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:9090")

def test_parameter():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/parameter", headers=HEADERS, timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        data = response.json()
        assert "theta" in data, "Key 'theta' not found in response"
        assert 0.95 <= data["theta"] <= 1.05, f"Expected theta between 0.95 and 1.05, got {data['theta']}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:9090")