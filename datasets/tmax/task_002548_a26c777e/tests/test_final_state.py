# test_final_state.py
import os
import json
import pytest

def test_libbackend_so_exists():
    path = "/home/user/project/libbackend.so"
    assert os.path.exists(path), f"File {path} is missing. The dummy library was not compiled."
    assert os.path.isfile(path), f"Expected {path} to be a file."

def test_test_report_json_exists():
    path = "/home/user/project/test_report.json"
    assert os.path.exists(path), f"File {path} is missing. Did you run pytest with JSON report generation?"
    assert os.path.isfile(path), f"Expected {path} to be a file."

def test_test_report_passed():
    path = "/home/user/project/test_report.json"
    if not os.path.exists(path):
        pytest.fail(f"Cannot check test results because {path} is missing.")

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not read or parse {path} as JSON: {e}")

    summary = data.get("summary", {})
    passed = summary.get("passed", 0)
    assert passed >= 1, f"Expected at least 1 passed test in the summary, but got {passed}. Full summary: {summary}"