# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_reachable_depth_0():
    try:
        response = requests.get(f"{BASE_URL}/reachable?depth=0", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")
    assert data == ["N-8392"], f"Expected ['N-8392'], got {data}"

def test_reachable_depth_1():
    try:
        response = requests.get(f"{BASE_URL}/reachable?depth=1", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")
    assert data == ["N-1000", "N-8392"], f"Expected ['N-1000', 'N-8392'], got {data}"

def test_reachable_depth_2():
    try:
        response = requests.get(f"{BASE_URL}/reachable?depth=2", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")
    assert data == ["N-1000", "N-2000", "N-3000", "N-8392"], f"Expected ['N-1000', 'N-2000', 'N-3000', 'N-8392'], got {data}"

def test_reachable_depth_3():
    try:
        response = requests.get(f"{BASE_URL}/reachable?depth=3", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")
    assert data == ["N-1000", "N-2000", "N-3000", "N-4000", "N-8392"], f"Expected ['N-1000', 'N-2000', 'N-3000', 'N-4000', 'N-8392'], got {data}"