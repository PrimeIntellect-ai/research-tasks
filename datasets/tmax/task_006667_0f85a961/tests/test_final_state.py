# test_final_state.py

import os
import json
import pytest

def test_summary_json_exists_and_correct():
    summary_path = '/home/user/summary.json'
    assert os.path.exists(summary_path), f"Expected output file {summary_path} does not exist. Did you run your script and generate it?"
    assert os.path.isfile(summary_path), f"{summary_path} is not a regular file."

    try:
        with open(summary_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {summary_path} as JSON: {e}")

    assert isinstance(data, dict), f"JSON content in {summary_path} must be a dictionary/object."

    # Verify external_port
    assert 'external_port' in data, "Key 'external_port' is missing from summary.json."
    assert data['external_port'] == 5522, f"Expected external_port to be 5522, got {data['external_port']}."

    # Verify disk_usage_pct
    assert 'disk_usage_pct' in data, "Key 'disk_usage_pct' is missing from summary.json."
    assert data['disk_usage_pct'] == 92, f"Expected disk_usage_pct to be 92, got {data['disk_usage_pct']}."

    # Verify service_status
    assert 'service_status' in data, "Key 'service_status' is missing from summary.json."
    assert data['service_status'] == "OK-DELAYED", f"Expected service_status to be 'OK-DELAYED', got '{data['service_status']}'."

def test_diagnose_script_exists():
    script_path = '/home/user/diagnose.py'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."