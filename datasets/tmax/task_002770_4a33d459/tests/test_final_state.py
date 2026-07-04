# test_final_state.py
import requests
import pytest
import time

def test_exfiltration_report():
    """Verify that the HTTP server returns the correct JSON report."""
    url = "http://127.0.0.1:8333/exfiltration-report"

    # Attempt to connect to the server with retries
    response = None
    for _ in range(5):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            time.sleep(1)

    if response is None:
        pytest.fail("Failed to connect to the HTTP server at 127.0.0.1:8333")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert data.get("investigator") == "log-analyst-1", f"Expected investigator 'log-analyst-1', got {data.get('investigator')}"
    assert data.get("target_ip") == "192.168.55.104", f"Expected target_ip '192.168.55.104', got {data.get('target_ip')}"

    hourly_exfiltration = data.get("hourly_exfiltration", {})
    assert isinstance(hourly_exfiltration, dict), "hourly_exfiltration must be a dictionary"

    assert hourly_exfiltration.get("2023-10-04T08") == 7500, f"Expected 7500 bytes for 2023-10-04T08, got {hourly_exfiltration.get('2023-10-04T08')}"
    assert hourly_exfiltration.get("2023-10-04T09") == 8000, f"Expected 8000 bytes for 2023-10-04T09, got {hourly_exfiltration.get('2023-10-04T09')}"