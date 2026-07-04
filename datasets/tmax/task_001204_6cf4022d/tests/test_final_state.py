# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_reachable_endpoint_A():
    url = f"{BASE_URL}/api/reachable?account=A"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "reachable" in data, f"Response missing 'reachable' key: {data}"

    reachable = data["reachable"]
    assert isinstance(reachable, list), f"'reachable' should be a list, got {type(reachable)}"

    expected = {"A", "B", "C", "D"}
    actual = set(reachable)
    assert actual == expected, f"Expected reachable accounts {expected}, got {actual}"

def test_reachable_endpoint_X():
    url = f"{BASE_URL}/api/reachable?account=X"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "reachable" in data, f"Response missing 'reachable' key: {data}"

    expected = {"Y", "Z"}
    actual = set(data["reachable"])
    assert actual == expected, f"Expected reachable accounts {expected}, got {actual}"

def test_volume_endpoint_page_1():
    url = f"{BASE_URL}/api/volume?page=1&limit=2"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "data" in data, f"Response missing 'data' key: {data}"
    assert "page" in data, f"Response missing 'page' key: {data}"

    assert data["page"] == 1, f"Expected page 1, got {data['page']}"

    expected_data = [
        {"account": "Y", "volume": 1500},
        {"account": "X", "volume": 1000}
    ]

    assert data["data"] == expected_data, f"Expected data {expected_data}, got {data['data']}"

def test_volume_endpoint_page_2():
    url = f"{BASE_URL}/api/volume?page=2&limit=2"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "data" in data, f"Response missing 'data' key: {data}"
    assert "page" in data, f"Response missing 'page' key: {data}"

    assert data["page"] == 2, f"Expected page 2, got {data['page']}"

    expected_data = [
        {"account": "D", "volume": 700},
        {"account": "C", "volume": 650}
    ]

    assert data["data"] == expected_data, f"Expected data {expected_data}, got {data['data']}"

def test_volume_endpoint_page_3():
    url = f"{BASE_URL}/api/volume?page=3&limit=3"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "data" in data, f"Response missing 'data' key: {data}"
    assert "page" in data, f"Response missing 'page' key: {data}"

    assert data["page"] == 3, f"Expected page 3, got {data['page']}"

    expected_data = [
        {"account": "Z", "volume": 500},
        {"account": "E", "volume": 400},
        {"account": "B", "volume": 300}
    ]

    assert data["data"] == expected_data, f"Expected data {expected_data}, got {data['data']}"

def test_bad_requests():
    # Missing account parameter
    url = f"{BASE_URL}/api/reachable"
    response = requests.get(url)
    assert response.status_code == 400, f"Expected HTTP 400 for missing account param, got {response.status_code}"

    # Missing page parameter
    url = f"{BASE_URL}/api/volume?limit=10"
    response = requests.get(url)
    assert response.status_code == 400, f"Expected HTTP 400 for missing page param, got {response.status_code}"

    # Invalid limit parameter
    url = f"{BASE_URL}/api/volume?page=1&limit=abc"
    response = requests.get(url)
    assert response.status_code == 400, f"Expected HTTP 400 for invalid limit param, got {response.status_code}"