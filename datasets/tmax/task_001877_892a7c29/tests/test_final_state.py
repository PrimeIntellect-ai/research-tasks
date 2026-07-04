# test_final_state.py

import os
import json
import pytest

def test_files_renamed():
    """Check that the correct files were renamed to .archived."""
    expected_archived = [
        "/home/user/data/file1.bin.archived",
        "/home/user/data/file3.bin.archived",
    ]
    for path in expected_archived:
        assert os.path.isfile(path), f"Expected archived file {path} does not exist. Was it renamed?"

    expected_missing = [
        "/home/user/data/file1.bin",
        "/home/user/data/file3.bin",
    ]
    for path in expected_missing:
        assert not os.path.exists(path), f"Original file {path} still exists. It should have been renamed."

def test_files_not_renamed():
    """Check that files not matching the criteria were not renamed."""
    expected_untouched = [
        "/home/user/data/file2.bin",
        "/home/user/data/file4.bin",
    ]
    for path in expected_untouched:
        assert os.path.isfile(path), f"File {path} is missing, but it should not have been renamed."
        archived_path = path + ".archived"
        assert not os.path.exists(archived_path), f"File {archived_path} exists, but it should not have been renamed."

def test_json_report():
    """Check that the JSON report exists and contains the correct sorted list of original paths."""
    report_path = "/home/user/archived_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    expected_data = [
        "/home/user/data/file1.bin",
        "/home/user/data/file3.bin",
    ]

    assert isinstance(data, list), f"Expected JSON report to be a list, got {type(data).__name__}."
    assert data == expected_data, f"JSON report content mismatch. Expected {expected_data}, got {data}."