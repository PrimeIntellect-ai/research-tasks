# test_final_state.py

import requests
import pytest

URL = "http://127.0.0.1:8080/api/v1/flash-telemetry"
VALID_TOKEN = "SecretAdminToken99"

def test_unauthorized_missing_token():
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

def test_unauthorized_invalid_token():
    headers = {"Authorization": "Bearer InvalidToken123"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}"

def test_authorized_valid_response():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "flash_events" in data, "Response JSON missing 'flash_events' key"
    events = data["flash_events"]
    assert isinstance(events, list), "'flash_events' should be a list"

    assert len(events) == 3, f"Expected 3 flash events, got {len(events)}"

    # Check sorting
    frame_indices = [event.get("frame_index") for event in events]
    assert frame_indices == sorted(frame_indices), "Events are not sorted by frame_index in ascending order"

    expected_frames = [25, 42, 88]
    expected_alerts = ["alert_1", "alert_2", "alert_3"]

    for i, event in enumerate(events):
        assert event.get("frame_index") == expected_frames[i], f"Expected frame_index {expected_frames[i]}, got {event.get('frame_index')}"
        assert event.get("sensor_reading") == expected_alerts[i], f"Expected sensor_reading {expected_alerts[i]}, got {event.get('sensor_reading')}"

        brightness = event.get("brightness")
        assert isinstance(brightness, (int, float)), f"Brightness should be a number, got {type(brightness)}"
        assert brightness > 200.0, f"Expected brightness > 200.0, got {brightness}"
        # The truth expects 255.0, but we allow some tolerance for ffmpeg extraction differences
        assert 250.0 <= brightness <= 255.0, f"Expected brightness close to 255.0, got {brightness}"