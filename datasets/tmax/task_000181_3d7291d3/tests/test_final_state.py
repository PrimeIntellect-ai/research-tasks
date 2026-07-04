# test_final_state.py

import pytest
import requests
import time

def test_api_events_endpoint():
    """Verify that the HTTP server is running and returns the correct events."""
    url = "http://127.0.0.1:8080/api/events"

    # Retry a few times in case the server is slow to start
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to the API at {url} after {max_retries} attempts.")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Failed to parse response as JSON.")

    assert "events" in data, "Response JSON is missing the 'events' key."
    events = data["events"]
    assert isinstance(events, list), "'events' should be a list."

    expected_events = [
        (1.50, 2.00),
        (4.20, 4.60),
        (7.80, 8.10)
    ]

    assert len(events) == len(expected_events), f"Expected {len(expected_events)} events, got {len(events)}."

    tolerance = 0.05
    for i, expected in enumerate(expected_events):
        actual = events[i]
        assert "start" in actual, f"Event {i} is missing 'start' key."
        assert "end" in actual, f"Event {i} is missing 'end' key."

        actual_start = actual["start"]
        actual_end = actual["end"]

        expected_start, expected_end = expected

        assert abs(actual_start - expected_start) <= tolerance, \
            f"Event {i} start time {actual_start} is outside tolerance of {expected_start} +/- {tolerance}"
        assert abs(actual_end - expected_end) <= tolerance, \
            f"Event {i} end time {actual_end} is outside tolerance of {expected_end} +/- {tolerance}"