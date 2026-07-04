# test_final_state.py
import requests
import pytest
import time

def test_server_listening_and_responses():
    # Allow a brief moment in case the server needs to initialize
    time.sleep(1)

    # Test case 1: A to D
    url1 = "http://127.0.0.1:9000/path?start=A&end=D"
    try:
        resp1 = requests.get(url1, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect or retrieve data from {url1}. Is the server running? Error: {e}")

    assert resp1.status_code == 200, f"Expected HTTP 200 OK for A->D, got {resp1.status_code}. Response: {resp1.text}"

    try:
        data1 = resp1.json()
    except ValueError:
        pytest.fail(f"Response from A->D is not valid JSON. Response text: {resp1.text}")

    expected_path_1 = ["A", "B", "C", "D"]
    expected_cost_1 = 6
    assert data1.get("path") == expected_path_1, f"Incorrect path for A->D. Expected {expected_path_1}, got {data1.get('path')}"
    assert data1.get("cost") == expected_cost_1, f"Incorrect cost for A->D. Expected {expected_cost_1}, got {data1.get('cost')}"

    # Test case 2: 1 to 3
    url2 = "http://127.0.0.1:9000/path?start=1&end=3"
    try:
        resp2 = requests.get(url2, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect or retrieve data from {url2}. Error: {e}")

    assert resp2.status_code == 200, f"Expected HTTP 200 OK for 1->3, got {resp2.status_code}. Response: {resp2.text}"

    try:
        data2 = resp2.json()
    except ValueError:
        pytest.fail(f"Response from 1->3 is not valid JSON. Response text: {resp2.text}")

    expected_path_2 = ["1", "4", "5", "3"]
    expected_cost_2 = 8
    assert data2.get("path") == expected_path_2, f"Incorrect path for 1->3. Expected {expected_path_2}, got {data2.get('path')}"
    assert data2.get("cost") == expected_cost_2, f"Incorrect cost for 1->3. Expected {expected_cost_2}, got {data2.get('cost')}"