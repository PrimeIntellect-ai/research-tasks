# test_final_state.py

import pytest
import requests
import time

INGEST_URL = "http://localhost:8080/ingest"
METRICS_URL = "http://localhost:8080/metrics"

def wait_for_service(url, timeout=5):
    """Wait for the service to be up and returning a non-error code on a basic request, or just accept connection."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # We just want to see if the port is open and responding to HTTP
            requests.get("http://localhost:8080/", timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_system_behavior():
    # Wait for Nginx to be up
    assert wait_for_service("http://localhost:8080/"), "Nginx/App is not reachable on port 8080"

    # 1. Send POST request to /ingest
    payload = (
        '{"timestamp": "2023-10-01T12:00:00Z", "data": "{\\"key\\": \\"val1\\"}"}\n'
        '{"timestamp": "2023-10-01T12:00:30Z", "data": "{\\"key\\": \\"val1\\"}"}\n'
        '{"timestamp": "2023-10-01T12:01:15Z", "data": "{\\"key\\": \\"m\\u00fcsta\\u00f1\\"}"}\n'
        '{"timestamp": "2023-10-01T12:04:45Z", "data": "{\\"key\\": \\"val3\\"}"}'
    )

    try:
        post_resp = requests.post(INGEST_URL, data=payload.encode('utf-8'), headers={"Content-Type": "application/json"}, timeout=5)
        assert post_resp.status_code in (200, 201, 202, 204), f"POST /ingest failed with status {post_resp.status_code}: {post_resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST /ingest request failed: {e}")

    # 2. Send GET request to /metrics
    params = {
        "start": "2023-10-01T11:58:00Z",
        "end": "2023-10-01T12:05:00Z"
    }
    try:
        get_resp = requests.get(METRICS_URL, params=params, timeout=5)
        assert get_resp.status_code == 200, f"GET /metrics failed with status {get_resp.status_code}: {get_resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"GET /metrics request failed: {e}")

    # 3. Assert Response
    try:
        data = get_resp.json()
    except ValueError:
        pytest.fail(f"GET /metrics did not return valid JSON. Response text: {get_resp.text}")

    expected_data = [
        {"minute": "2023-10-01T11:58:00Z", "changes": 0, "rolling_5m_count": 0},
        {"minute": "2023-10-01T11:59:00Z", "changes": 0, "rolling_5m_count": 0},
        {"minute": "2023-10-01T12:00:00Z", "changes": 1, "rolling_5m_count": 1},
        {"minute": "2023-10-01T12:01:00Z", "changes": 1, "rolling_5m_count": 2},
        {"minute": "2023-10-01T12:02:00Z", "changes": 0, "rolling_5m_count": 2},
        {"minute": "2023-10-01T12:03:00Z", "changes": 0, "rolling_5m_count": 2},
        {"minute": "2023-10-01T12:04:00Z", "changes": 1, "rolling_5m_count": 3},
        {"minute": "2023-10-01T12:05:00Z", "changes": 0, "rolling_5m_count": 2}
    ]

    assert isinstance(data, list), f"Expected response to be a list, got {type(data)}"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}. Data: {data}"

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert actual_item.get("minute") == expected_item["minute"], f"Mismatch at index {i}: expected minute {expected_item['minute']}, got {actual_item.get('minute')}"
        assert actual_item.get("changes") == expected_item["changes"], f"Mismatch at index {i} ({expected_item['minute']}): expected changes {expected_item['changes']}, got {actual_item.get('changes')}"
        assert actual_item.get("rolling_5m_count") == expected_item["rolling_5m_count"], f"Mismatch at index {i} ({expected_item['minute']}): expected rolling_5m_count {expected_item['rolling_5m_count']}, got {actual_item.get('rolling_5m_count')}"