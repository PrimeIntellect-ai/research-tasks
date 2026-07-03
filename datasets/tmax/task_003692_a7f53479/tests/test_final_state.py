# test_final_state.py

import os
import json
import pytest

APP_DIR = "/home/user/app"
SUMMARY_JSON_PATH = os.path.join(APP_DIR, "summary.json")
PARSER_PY_PATH = os.path.join(APP_DIR, "parser.py")

def test_parser_py_exists():
    """Test that the student created parser.py."""
    assert os.path.isfile(PARSER_PY_PATH), (
        f"File {PARSER_PY_PATH} is missing. You need to write a corrected "
        "parser.py file to replace the functionality of the .pyc file."
    )

def test_summary_json_exists():
    """Test that main.py was run successfully and generated summary.json."""
    assert os.path.isfile(SUMMARY_JSON_PATH), (
        f"File {SUMMARY_JSON_PATH} is missing. Did you run main.py successfully?"
    )

def test_summary_json_content():
    """Test that summary.json contains the correct event_count and last_ts."""
    with open(SUMMARY_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUMMARY_JSON_PATH} does not contain valid JSON.")

    assert "event_count" in data, "Key 'event_count' is missing in summary.json."
    assert "last_ts" in data, "Key 'last_ts' is missing in summary.json."

    expected_event_count = 4
    expected_last_ts = 2147483700

    assert data["event_count"] == expected_event_count, (
        f"Expected event_count to be {expected_event_count}, but got {data['event_count']}."
    )
    assert data["last_ts"] == expected_last_ts, (
        f"Expected last_ts to be {expected_last_ts}, but got {data['last_ts']}. "
        "Ensure you are unpacking the binary data as unsigned integers to prevent overflow."
    )