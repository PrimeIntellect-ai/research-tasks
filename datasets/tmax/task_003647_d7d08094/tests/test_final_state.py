# test_final_state.py

import os
import json
import pytest

def test_unified_timeouts_json_exists():
    """Test that the unified_timeouts.json file exists."""
    assert os.path.isfile("/home/user/unified_timeouts.json"), "/home/user/unified_timeouts.json is missing"

def test_unified_timeouts_json_content():
    """Test that the unified_timeouts.json file contains the correct sorted list of timeouts."""
    try:
        with open("/home/user/unified_timeouts.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("/home/user/unified_timeouts.json is not valid JSON")

    expected_data = [
        {
            "timestamp": "2023-10-25T14:30:17.000Z",
            "service": "payment",
            "message": "データベース タイムアウト"
        },
        {
            "timestamp": "2023-10-25T14:30:18.000Z",
            "service": "auth",
            "message": "Connection timeout"
        },
        {
            "timestamp": "2023-10-25T14:30:20.000Z",
            "service": "auth",
            "message": "Request Timeout on API"
        },
        {
            "timestamp": "2023-10-25T14:30:22.000Z",
            "service": "payment",
            "message": "ネットワーク タイムアウト"
        }
    ]

    assert isinstance(data, list), "The JSON output should be a list"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, f"Mismatch at index {i}. Expected: {expected}, Got: {actual}"

def test_pipeline_log_exists_and_content():
    """Test that pipeline.log exists and contains the correct success message."""
    pipeline_log_path = "/home/user/pipeline.log"
    assert os.path.isfile(pipeline_log_path), f"{pipeline_log_path} is missing"

    with open(pipeline_log_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_message = "[SUCCESS] Processed logs: auth timeouts: 2, payment timeouts: 2"
    assert expected_message in content, f"pipeline.log does not contain the expected success message. Found: {content}"