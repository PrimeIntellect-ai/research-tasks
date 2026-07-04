# test_final_state.py

import pytest
import requests
import time

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_server_running_and_responds():
    """Test that the server is running on 127.0.0.1:8080 and responds correctly to the first query."""
    base_url = "http://127.0.0.1:8080"

    # Wait for server to be up (in case it's slow to start, though it should be running)
    server_up = wait_for_server(f"{base_url}/") or wait_for_server(f"{base_url}/restore_path?source=5&dest=50")
    assert server_up, "Server is not running or not reachable at 127.0.0.1:8080"

    # Query 1: source=5, dest=50
    url1 = f"{base_url}/restore_path?source=5&dest=50"
    try:
        resp1 = requests.get(url1, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to server for query 1: {e}")

    assert resp1.status_code == 200, f"Expected status code 200, got {resp1.status_code}. Response: {resp1.text}"

    try:
        data1 = resp1.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp1.text}")

    assert "path" in data1, f"Missing 'path' in response: {data1}"
    assert "total_latency" in data1, f"Missing 'total_latency' in response: {data1}"
    assert data1["path"] == [5, 12, 50], f"Expected path [5, 12, 50], got {data1['path']}"
    assert data1["total_latency"] == 30, f"Expected total_latency 30, got {data1['total_latency']}"

def test_second_query():
    """Test the second query for shortest path."""
    base_url = "http://127.0.0.1:8080"

    # Query 2: source=12, dest=8
    url2 = f"{base_url}/restore_path?source=12&dest=8"
    try:
        resp2 = requests.get(url2, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to server for query 2: {e}")

    assert resp2.status_code == 200, f"Expected status code 200, got {resp2.status_code}. Response: {resp2.text}"

    try:
        data2 = resp2.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp2.text}")

    assert "path" in data2, f"Missing 'path' in response: {data2}"
    assert "total_latency" in data2, f"Missing 'total_latency' in response: {data2}"
    assert data2["path"] == [12, 8], f"Expected path [12, 8], got {data2['path']}"
    assert data2["total_latency"] == 5, f"Expected total_latency 5, got {data2['total_latency']}"

def test_no_path():
    """Test that a non-existent path returns a 404."""
    base_url = "http://127.0.0.1:8080"
    url = f"{base_url}/restore_path?source=5&dest=99"
    try:
        resp = requests.get(url, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to server for no-path query: {e}")

    assert resp.status_code == 404, f"Expected status code 404 for no path, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "error" in data, f"Missing 'error' key in 404 response: {data}"