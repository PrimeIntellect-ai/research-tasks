# test_final_state.py

import os
import json
import pytest

def test_local_logs_copied():
    """Verify that the logs were copied to the local directory."""
    local_dir = '/home/user/local_logs'
    assert os.path.isdir(local_dir), f"Directory {local_dir} does not exist."

    # Check that server1.txt and server2.txt are present
    assert os.path.isfile(os.path.join(local_dir, 'server1.txt')), "server1.txt was not copied to local_logs."
    assert os.path.isfile(os.path.join(local_dir, 'server2.txt')), "server2.txt was not copied to local_logs."

def test_process_logs_script_exists():
    """Verify that the python script was created."""
    script_path = '/home/user/process_logs.py'
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

def test_sampled_logs_json():
    """Verify the final output JSON is correct."""
    output_path = '/home/user/sampled_logs.json'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    expected_data = [
        {
            "timestamp": "2024-02-14T13:00:00Z",
            "severity": "INFO",
            "message": "User logged in"
        },
        {
            "timestamp": "2024-02-14T15:00:00Z",
            "severity": "WARNING",
            "message": "Disk space low"
        },
        {
            "timestamp": "2024-02-14T15:30:00Z",
            "severity": "ERROR",
            "message": "Database connection failed"
        },
        {
            "timestamp": "2024-02-14T19:15:00Z",
            "severity": "CRITICAL",
            "message": "System crash"
        }
    ]

    assert isinstance(data, list), "The JSON output must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in the JSON array, found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("timestamp") == expected["timestamp"], f"Item {i}: Expected timestamp {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual.get("severity") == expected["severity"], f"Item {i}: Expected severity {expected['severity']}, got {actual.get('severity')}"
        assert actual.get("message") == expected["message"], f"Item {i}: Expected message '{expected['message']}', got '{actual.get('message')}'"

def test_cron_setup():
    """Verify the cron setup file contains the exact expected string."""
    cron_path = '/home/user/cron_setup.txt'
    assert os.path.isfile(cron_path), f"Cron setup file {cron_path} does not exist."

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    expected_cron = "45 * * * * /usr/bin/python3 /home/user/process_logs.py"
    assert content == expected_cron, f"Cron setup file content is incorrect. Expected: '{expected_cron}', Got: '{content}'"