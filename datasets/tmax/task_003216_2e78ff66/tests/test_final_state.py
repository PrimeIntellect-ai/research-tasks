# test_final_state.py
import os
import json
import pytest

BASE_DIR = "/home/user/telemetry_processor"
SUMMARY_PATH = os.path.join(BASE_DIR, "summary.json")
REQ_PATH = os.path.join(BASE_DIR, "requirements.txt")

def test_summary_json_exists():
    assert os.path.isfile(SUMMARY_PATH), f"Expected output file {SUMMARY_PATH} does not exist."

def test_summary_json_content():
    with open(SUMMARY_PATH, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUMMARY_PATH} is not a valid JSON file.")

    expected = {
        "total_events_processed": 5,
        "unique_event_ids": 5,
        "total_value": 150
    }

    assert summary.get("total_events_processed") == expected["total_events_processed"], \
        f"Expected total_events_processed to be {expected['total_events_processed']}, got {summary.get('total_events_processed')}"

    assert summary.get("unique_event_ids") == expected["unique_event_ids"], \
        f"Expected unique_event_ids to be {expected['unique_event_ids']}, got {summary.get('unique_event_ids')}"

    assert summary.get("total_value") == expected["total_value"], \
        f"Expected total_value to be {expected['total_value']}, got {summary.get('total_value')}"

def test_requirements_fixed():
    assert os.path.isfile(REQ_PATH), f"Requirements file {REQ_PATH} is missing."
    with open(REQ_PATH, 'r') as f:
        content = f.read()

    # numpy==1.20.0 was the original conflicting version. It should be changed.
    assert "numpy==1.20.0" not in content, "requirements.txt still contains the conflicting numpy==1.20.0 version."
    assert "numpy" in content.lower(), "requirements.txt must still contain numpy."
    assert "pandas" in content.lower(), "requirements.txt must still contain pandas."

def test_process_py_modified():
    process_path = os.path.join(BASE_DIR, "process.py")
    assert os.path.isfile(process_path), f"File {process_path} does not exist."

    with open(process_path, 'r') as f:
        content = f.read()

    # We don't check exact implementation details of the fix, but we can ensure 
    # the file is still present and basic structure remains.
    assert "def flatten_events" in content, "process.py is missing flatten_events function."
    assert "def main" in content, "process.py is missing main function."