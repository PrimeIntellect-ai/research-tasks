# test_final_state.py

import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = f"{BASE_URL}/api/v1/translations/process"
AUTH_HEADER = {"Authorization": "Bearer LOCALIZATION_ENGINEER_TOKEN_99"}

def test_unauthorized_access():
    """Test that requests without the correct token are rejected with 401."""
    try:
        response = requests.post(ENDPOINT, json=[])
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:8080")

def test_gap_imputation_and_rolling_stats():
    """Test gap imputation and rolling stats over a sequence of segments."""
    payload = [
        {"startTime": 0.0, "endTime": 2.0, "text": "Segment 1", "confidence": 0.9},
        {"startTime": 4.5, "endTime": 6.0, "text": "Segment 2", "confidence": 0.8},
        {"startTime": 6.0, "endTime": 7.0, "text": "Segment 3", "confidence": 0.7},
        {"startTime": 7.0, "endTime": 8.0, "text": "Segment 4", "confidence": 0.9}
    ]

    response = requests.post(ENDPOINT, json=payload, headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()

    # We expect 5 segments (4 original + 1 interpolated)
    assert len(data) >= 5, "Expected at least 5 segments (including interpolated gap)"

    # Check for gap imputation between 2.0 and 4.5
    has_imputed = False
    for seg in data:
        if math.isclose(seg.get("startTime", 0), 2.0, abs_tol=0.1) and math.isclose(seg.get("endTime", 0), 4.5, abs_tol=0.1):
            has_imputed = True
            break
    assert has_imputed, "Gap imputation missing or incorrect for gap between 2.0s and 4.5s"

def test_scene_boundary_and_duration_constraints():
    """Test scene boundary adjustment and max duration constraints."""
    payload = [
        # This segment overlaps the scene boundary (12.5 - 13.0)
        {"startTime": 10.0, "endTime": 12.8, "text": "Overlap segment", "confidence": 0.9},
        # This segment is too long (> 7s)
        {"startTime": 15.0, "endTime": 24.0, "text": "Long segment", "confidence": 0.9}
    ]

    response = requests.post(ENDPOINT, json=payload, headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()

    # Check overlap adjustment
    overlap_seg = next((s for s in data if s.get("text") == "Overlap segment"), None)
    assert overlap_seg is not None, "Overlap segment missing from response"
    assert overlap_seg["endTime"] <= 12.5, f"Expected endTime to be adjusted to <= 12.5, got {overlap_seg['endTime']}"

    # Check duration constraint
    long_seg = next((s for s in data if s.get("text") == "Long segment"), None)
    if long_seg:
        duration = long_seg["endTime"] - long_seg["startTime"]
        assert duration <= 7.0, f"Expected segment duration <= 7.0s, got {duration}s"