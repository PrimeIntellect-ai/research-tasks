# test_final_state.py
import os
import json
import pytest

def test_siem_ingest_json_exists():
    path = "/home/user/siem_ingest.json"
    assert os.path.exists(path), f"File {path} does not exist. The Go program may not have successfully POSTed to the SIEM endpoint."
    assert os.path.isfile(path), f"{path} is not a regular file."

def test_siem_ingest_content():
    path = "/home/user/siem_ingest.json"
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {path}: {e}")

    assert isinstance(data, list), "The JSON payload should be an array of objects."
    assert len(data) == 3, f"Expected exactly 3 deduplicated error objects, but found {len(data)}."

    expected_objects = [
        {
            "timestamp": "2023-10-12T08:15:00Z",
            "code": "1052",
            "message": "Database connection timeout"
        },
        {
            "timestamp": "2023-10-12T08:17:33Z",
            "code": "2099",
            "message": "User auth failed: invalid token"
        },
        {
            "timestamp": "2023-10-12T08:19:12Z",
            "code": "3001",
            "message": "File not found: /etc/passwd"
        }
    ]

    # Check that each expected object is in the parsed JSON data
    # Order might vary depending on how they serialized, but chronologically they should match.
    # We will just assert the exact list matches to ensure chronological order is preserved.
    assert data == expected_objects, "The parsed JSON does not match the expected deduplicated error objects or is in the wrong order."