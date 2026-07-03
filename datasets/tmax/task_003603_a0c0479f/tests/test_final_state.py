# test_final_state.py

import json
import pytest
import requests
import math

def test_api_records_endpoint():
    """Verify that the API is running and returning the correctly processed data."""
    url = "http://127.0.0.1:8000/api/records"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), "Expected the JSON response to be a list of objects"
    assert len(data) == 5, f"Expected 5 records, got {len(data)}"

    expected_tokens = {
        1: "EVT_500",
        2: "EVT_UNK",
        3: "EVT_502",
        4: "EVT_404",
        5: "EVT_UNK"
    }

    for row in data:
        assert isinstance(row, dict), "Each record must be a JSON object"
        assert "id" in row, "Missing 'id' field in record"
        assert "token" in row, "Missing 'token' field in record"
        assert "video_frames" in row, "Missing 'video_frames' field in record"

        row_id = row["id"]
        assert row_id in expected_tokens, f"Unexpected id {row_id} in record"

        expected_token = expected_tokens[row_id]
        actual_token = row["token"]
        assert actual_token == expected_token, f"For id {row_id}, expected token '{expected_token}', got '{actual_token}'"

        actual_frames = row["video_frames"]
        assert actual_frames == 120, f"For id {row_id}, expected video_frames to be 120, got {actual_frames}"