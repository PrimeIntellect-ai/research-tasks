# test_final_state.py

import os
import json
import pytest

def test_output_fast_exists():
    path = "/home/user/output_fast.npy"
    assert os.path.isfile(path), f"Expected file {path} to exist."

def test_report_json_exists_and_content():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "passed" in report, f"Key 'passed' missing in {path}."
    assert "p_value" in report, f"Key 'p_value' missing in {path}."

    assert report["passed"] is True, f"Expected 'passed' to be True, got {report['passed']}."
    assert report["p_value"] == 1.0, f"Expected 'p_value' to be 1.0, got {report['p_value']}."

def test_simulate_uses_multiprocessing():
    path = "/home/user/simulate.py"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "multiprocessing" in content, f"Expected to find 'multiprocessing' in {path}."