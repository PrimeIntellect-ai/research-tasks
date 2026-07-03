# test_final_state.py

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server(url, timeout=5):
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def check_server_up():
    assert wait_for_server(f"{BASE_URL}/"), f"Could not connect to API server at {BASE_URL}. Is it running?"

def test_upstream_omega():
    url = f"{BASE_URL}/upstream?dataset=OMEGA"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected status 200 from {url}, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "upstream" in data, f"Key 'upstream' missing in response from {url}. Got: {data}"
    expected = ["ALPHA", "BETA", "DELTA", "GAMMA", "RHO", "THETA"]
    assert data["upstream"] == expected, f"Expected upstream for OMEGA to be {expected}, got {data['upstream']}"

def test_downstream_alpha():
    url = f"{BASE_URL}/downstream?dataset=ALPHA"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected status 200 from {url}, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "downstream" in data, f"Key 'downstream' missing in response from {url}. Got: {data}"
    expected = ["BETA", "DELTA", "GAMMA", "OMEGA"]
    assert data["downstream"] == expected, f"Expected downstream for ALPHA to be {expected}, got {data['downstream']}"

def test_upstream_alpha():
    url = f"{BASE_URL}/upstream?dataset=ALPHA"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected status 200 from {url}, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "upstream" in data, f"Key 'upstream' missing in response from {url}. Got: {data}"
    expected = []
    assert data["upstream"] == expected, f"Expected upstream for ALPHA to be {expected}, got {data['upstream']}"

def test_downstream_omega():
    url = f"{BASE_URL}/downstream?dataset=OMEGA"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected status 200 from {url}, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "downstream" in data, f"Key 'downstream' missing in response from {url}. Got: {data}"
    expected = []
    assert data["downstream"] == expected, f"Expected downstream for OMEGA to be {expected}, got {data['downstream']}"