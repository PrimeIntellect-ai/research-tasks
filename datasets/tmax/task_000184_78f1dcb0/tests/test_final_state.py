# test_final_state.py

import os
import requests

def test_service_ready_file():
    assert os.path.isfile("/home/user/service_ready.txt"), "/home/user/service_ready.txt does not exist. Did you create it after starting the server?"

def test_analyze_mesh_endpoint():
    url = "http://127.0.0.1:8080/analyze_mesh"

    # Test case 1: Region 1 (0-100, 0-100) -> 2 Hz, baseline 2.0 -> Not divergent
    payload1 = {"x_min": 0, "y_min": 0, "x_max": 100, "y_max": 100}
    try:
        resp1 = requests.post(url, json=payload1, timeout=15)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service at {url}. Is it running? Error: {e}"

    assert resp1.status_code == 200, f"Expected HTTP 200, got {resp1.status_code}. Response body: {resp1.text}"

    try:
        data1 = resp1.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {resp1.text}"

    assert "dominant_frequency" in data1, "Missing 'dominant_frequency' in response"
    assert "is_divergent" in data1, "Missing 'is_divergent' in response"

    assert abs(data1["dominant_frequency"] - 2.0) < 0.1, f"Expected dominant_frequency ~2.0, got {data1['dominant_frequency']}"
    assert data1["is_divergent"] is False, f"Expected is_divergent to be False, got {data1['is_divergent']}"

    # Test case 2: Region 2 (100-200, 100-200) -> 5 Hz, baseline 5.5 -> Divergent
    payload2 = {"x_min": 100, "y_min": 100, "x_max": 200, "y_max": 200}
    resp2 = requests.post(url, json=payload2, timeout=15)
    assert resp2.status_code == 200, f"Expected HTTP 200, got {resp2.status_code}. Response body: {resp2.text}"
    data2 = resp2.json()

    assert abs(data2["dominant_frequency"] - 5.0) < 0.1, f"Expected dominant_frequency ~5.0, got {data2['dominant_frequency']}"
    assert data2["is_divergent"] is True, f"Expected is_divergent to be True, got {data2['is_divergent']}"

    # Test case 3: Region 3 (200-300, 200-300) -> 10 Hz, baseline 10.0 -> Not divergent
    payload3 = {"x_min": 200, "y_min": 200, "x_max": 300, "y_max": 300}
    resp3 = requests.post(url, json=payload3, timeout=15)
    assert resp3.status_code == 200, f"Expected HTTP 200, got {resp3.status_code}. Response body: {resp3.text}"
    data3 = resp3.json()

    assert abs(data3["dominant_frequency"] - 10.0) < 0.1, f"Expected dominant_frequency ~10.0, got {data3['dominant_frequency']}"
    assert data3["is_divergent"] is False, f"Expected is_divergent to be False, got {data3['is_divergent']}"