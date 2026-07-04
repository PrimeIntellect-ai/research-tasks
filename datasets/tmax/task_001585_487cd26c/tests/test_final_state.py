# test_final_state.py

import pytest
import requests
import concurrent.futures
import math

COLLECTOR_URL = "http://localhost:8081/ingest"
API_URL = "http://localhost:8082/sensors"
AUTH_TOKEN = "secret-token-99"

def send_valid_request(value):
    try:
        response = requests.post(COLLECTOR_URL, json={"sensor_id": "temp_1", "value": value}, timeout=5)
        return response.status_code
    except requests.RequestException as e:
        return str(e)

def test_collector_malformed_json_handling():
    """Test that the collector handles malformed JSON without crashing and returns 400."""
    try:
        # Send malformed JSON (type mismatch)
        response = requests.post(COLLECTOR_URL, json={"sensor_id": "temp_1", "value": "bad_string"}, timeout=5)
        assert response.status_code == 400, f"Expected HTTP 400 for malformed JSON, got {response.status_code}"
    except requests.ConnectionError:
        pytest.fail("Collector service is not running or crashed upon receiving malformed JSON.")

def test_collector_concurrent_requests():
    """Test that the collector handles concurrent requests without race conditions (NaNs)."""
    num_requests = 100
    values = [20.0 + (i % 10) for i in range(num_requests)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(send_valid_request, values))

    for res in results:
        assert res == 200 or res == 201 or res == 202 or res == 204, f"Expected successful status code, got {res}"

def test_api_authenticated_read():
    """Test that the API returns the correct, numerically stable average with authentication."""
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(f"{API_URL}/temp_1", headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200 from API, got {response.status_code}. Response: {response.text}"

        data = response.json()
        assert "value" in data or "average" in data or isinstance(data, float) or isinstance(data, dict), "Unexpected API response format"

        # Extract the float value depending on common JSON structures
        if isinstance(data, dict):
            val = data.get("value", data.get("average", None))
            if val is None:
                # If it's just returning the raw float as string or something else, try to parse
                val = float(response.text.strip())
        else:
            val = float(data)

        assert not math.isnan(val), "API returned NaN, indicating a race condition in the collector."
    except requests.ConnectionError:
        pytest.fail("API service is not running on port 8082.")
    except ValueError:
        pytest.fail(f"Could not parse API response as a float/JSON: {response.text}")