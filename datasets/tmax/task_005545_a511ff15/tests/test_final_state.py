# test_final_state.py

import os
import json
import pytest

REPORT_PATH = '/home/user/report.json'

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Expected output file {REPORT_PATH} does not exist."

def test_report_valid_json():
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} does not contain valid JSON.")
    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."

def test_report_contents():
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    expected_data = [
        {
            "filename": "01_init.snap",
            "version": 1,
            "commit": "7a8f9e0",
            "author": "sysadmin",
            "changes": [
                "Initial deployment",
                "Setup firewall rules"
            ]
        },
        {
            "filename": "03_update.snap",
            "version": 2,
            "commit": "b4c5d6e",
            "author": "devops_bob",
            "changes": [
                "Increased max connections",
                "Updated SSL certificates",
                "Removed old user accounts"
            ]
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} entries in the report, but found {len(data)}."

    # Check that the list is sorted by filename
    filenames = [entry.get('filename') for entry in data]
    assert filenames == sorted(filenames), "The JSON array is not sorted alphabetically by filename."

    for i, expected_entry in enumerate(expected_data):
        actual_entry = data[i]
        assert actual_entry.get("filename") == expected_entry["filename"], f"Mismatch in filename at index {i}."
        assert actual_entry.get("version") == expected_entry["version"], f"Mismatch in version at index {i}."
        assert actual_entry.get("commit") == expected_entry["commit"], f"Mismatch in commit at index {i}."
        assert actual_entry.get("author") == expected_entry["author"], f"Mismatch in author at index {i}."
        assert actual_entry.get("changes") == expected_entry["changes"], f"Mismatch in changes at index {i}."

def test_corrupt_file_skipped():
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        assert entry.get("filename") != "02_bad.snap", "Corrupt file '02_bad.snap' was not skipped."