# test_final_state.py
import pytest
import requests
import time
import json

def wait_for_service(url, timeout=10):
    """Wait for the HTTP service to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just checking if the port is open and responding to HTTP
            # We can use a GET to /anomalies or just check the connection
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_service_ingest_and_anomalies():
    base_url = "http://127.0.0.1:8282"

    # 1. Wait for the service to be up
    service_up = wait_for_service(f"{base_url}/anomalies")
    assert service_up, f"Service at {base_url} is not reachable after 10 seconds. Is it listening on port 8282?"

    # 2. Prepare payload
    # We want to create a clear anomaly at 10:09.
    # 10:00 to 10:08 -> 1 intl log each minute
    # 10:09 -> 20 intl logs
    # This guarantees an anomaly regardless of sample vs population std dev.
    payload = []

    # Background traffic (APAC)
    for i in range(9):
        payload.append({
            "timestamp": f"2023-10-01T10:0{i}:15",
            "ip": "10.0.0.1", # APAC
            "message": "こんにちは世界" # 7 non-ascii, 0 ascii -> is_intl = true
        })
        # Add some non-intl logs to ensure they are ignored in the count
        payload.append({
            "timestamp": f"2023-10-01T10:0{i}:30",
            "ip": "10.0.0.1",
            "message": "hello world" # 11 ascii, 0 non-ascii -> is_intl = false
        })

    # Anomaly traffic (APAC)
    for j in range(20):
        payload.append({
            "timestamp": f"2023-10-01T10:09:{j:02d}",
            "ip": "10.0.0.1",
            "message": "こんにちは世界"
        })

    # Another region (EMEA) with no anomalies
    for i in range(10):
        payload.append({
            "timestamp": f"2023-10-01T10:0{i}:15",
            "ip": "10.0.0.2", # EMEA
            "message": "こんにちは世界"
        })

    # 3. Post to /ingest
    try:
        ingest_resp = requests.post(f"{base_url}/ingest", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to POST /ingest: {e}")

    assert ingest_resp.status_code == 200, f"Expected POST /ingest to return HTTP 200, got {ingest_resp.status_code}. Response: {ingest_resp.text}"

    # 4. Get from /anomalies
    try:
        anomalies_resp = requests.get(f"{base_url}/anomalies", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to GET /anomalies: {e}")

    assert anomalies_resp.status_code == 200, f"Expected GET /anomalies to return HTTP 200, got {anomalies_resp.status_code}. Response: {anomalies_resp.text}"

    try:
        anomalies_data = anomalies_resp.json()
    except json.JSONDecodeError:
        pytest.fail(f"GET /anomalies did not return valid JSON. Response: {anomalies_resp.text}")

    # 5. Assert the anomaly
    # APAC should have an anomaly at 2023-10-01T10:09:00
    assert "APAC" in anomalies_data, f"Expected 'APAC' in anomalies response, got keys: {list(anomalies_data.keys())}"

    apac_anomalies = anomalies_data["APAC"]
    assert "2023-10-01T10:09:00" in apac_anomalies, f"Expected anomaly at '2023-10-01T10:09:00' for APAC, got: {apac_anomalies}"

    # Ensure EMEA has no anomalies
    if "EMEA" in anomalies_data:
        assert len(anomalies_data["EMEA"]) == 0, f"Expected no anomalies for EMEA, got: {anomalies_data['EMEA']}"