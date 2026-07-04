# test_final_state.py
import json
import os
import subprocess
import pytest

def test_forensics_report():
    report_path = "/home/user/forensics_report.json"
    assert os.path.exists(report_path), f"{report_path} not found."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {report_path} as valid JSON.")

    assert "secret_key" in data, "The key 'secret_key' is missing from forensics_report.json."
    assert data["secret_key"] == "TX99-CRASH-OVR", f"Incorrect secret key found: {data['secret_key']}."

    assert "crash_item_id" in data, "The key 'crash_item_id' is missing from forensics_report.json."
    assert data["crash_item_id"] == "REQ-8829", f"Incorrect crash item id found: {data['crash_item_id']}."

def test_reproduce_script():
    script_path = "/home/user/reproduce.py"
    assert os.path.exists(script_path), f"{script_path} not found."

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)

    assert result.returncode != 0, "reproduce.py executed successfully but was expected to crash."
    assert "CRITICAL FAILURE: Segfault triggered by poison pill input" in result.stderr, (
        "reproduce.py did not trigger the correct ValueError. "
        f"Stderr output was: {result.stderr}"
    )