# test_final_state.py

import base64
import json
import requests
import pytest

def test_service_extraction():
    url = "http://127.0.0.1:8080/extract"
    payload = {
        "video_path": "/app/diagnostic_feed.mp4",
        "t0": 2.0,
        "delta": 1.0,
        "n": 4
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {url}: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}. Response body: {resp.text}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response body: {resp.text}")

    assert "frames" in data, "Response JSON is missing the 'frames' key."

    frames = data["frames"]
    assert isinstance(frames, list), f"Expected 'frames' to be a list, got {type(frames)}."
    assert len(frames) == 4, f"Expected exactly 4 frames, got {len(frames)}."

    for i, b64_str in enumerate(frames):
        try:
            img_bytes = base64.b64decode(b64_str)
        except Exception as e:
            pytest.fail(f"Frame {i} is not a valid Base64 string: {e}")

        # Check for JPEG magic bytes (FF D8 FF)
        assert img_bytes.startswith(b'\xff\xd8\xff'), f"Frame {i} is not a valid JPEG image (missing magic bytes)."

        # Ensure the image has a reasonable size
        assert len(img_bytes) > 1024, f"Frame {i} is too small ({len(img_bytes)} bytes) to be a valid captured frame."