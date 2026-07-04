# test_final_state.py

import os
import json
import pytest

def test_build_artifacts_exist():
    """Verify that the Makefile was fixed and artifacts were built."""
    lib_path = "/home/user/project/libeval.so"
    bin_path = "/home/user/project/eval_tool"

    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}. Did the Makefile build successfully?"
    assert os.path.isfile(bin_path), f"Go executable not found at {bin_path}. Did the Makefile build successfully?"

def test_report_json_content():
    """Verify the contents of the generated report.json file."""
    report_path = "/home/user/report.json"

    assert os.path.isfile(report_path), f"Result file not found at {report_path}."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_data = {
        "ALPHA": 8,
        "BETA": 3,
        "DELTA": 25,
        "GAMMA": 100
    }

    assert data == expected_data, f"JSON content in {report_path} does not match the expected evaluated results."