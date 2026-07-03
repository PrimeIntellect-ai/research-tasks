# test_final_state.py
import time
import requests
import pytest

PAYLOAD = """100,A,5,ok
102,B,10,"this is
a broken
row"
105,C,15,ok
101,A,2,ok
106,B,20,"another
broken"
108,C,10,ok"""

def test_pipeline_processing():
    # Send data to the ingest service
    try:
        # The ingest service uses a simple `nc` command which might not return a valid HTTP response
        # or might close the connection abruptly. We catch exceptions to prevent the test from crashing here.
        requests.post("http://127.0.0.1:8080/", data=PAYLOAD, timeout=2)
    except requests.exceptions.RequestException:
        pass

    # Wait for the processing script to finish
    time.sleep(2)

    # Fetch the stats from the API service
    try:
        response = requests.get("http://127.0.0.1:8081/stats", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API service on port 8081 or request timed out: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API did not return valid JSON. Response text:\n{response.text}")

    assert "valid_rows" in data, "JSON response missing 'valid_rows' key"
    assert "rolling_sums" in data, "JSON response missing 'rolling_sums' key"

    assert data["valid_rows"] == 4, f"Expected 4 valid rows, got {data['valid_rows']}"
    assert data["rolling_sums"] == [5, 7, 22, 27], f"Expected rolling sums [5, 7, 22, 27], got {data['rolling_sums']}"