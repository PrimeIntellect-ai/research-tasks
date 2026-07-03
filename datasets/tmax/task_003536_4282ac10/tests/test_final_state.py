# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/generate_report.sh"
DB_PATH = "/home/user/analytics.db"

def test_script_exists_and_executable():
    """Test that the wrapper script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

    st = os.stat(SCRIPT_PATH)
    assert st.st_mode & stat.S_IXUSR, f"Script {SCRIPT_PATH} is not executable"

def test_script_execution_and_output():
    """Test executing the script and verify the JSON output."""
    output_path = "/home/user/test_report_1.json"
    if os.path.exists(output_path):
        os.remove(output_path)

    # Execute the script
    result = subprocess.run(
        ["/bin/bash", SCRIPT_PATH, "completed", "50", output_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"
    assert os.path.exists(output_path), f"Output JSON file was not created at {output_path}"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} does not contain valid JSON.")

    expected_data = [
        {
            "customer_name": "Charlie Brown",
            "total_spent": 300.0,
            "total_interaction_time": 0
        },
        {
            "customer_name": "Alice Smith",
            "total_spent": 250.0,
            "total_interaction_time": 120
        },
        {
            "customer_name": "Bob Jones",
            "total_spent": 100.0,
            "total_interaction_time": 300
        }
    ]

    assert isinstance(data, list), "Output JSON must be an array of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("customer_name") == expected["customer_name"], f"Record {i}: Expected customer_name '{expected['customer_name']}', got '{actual.get('customer_name')}'"
        assert float(actual.get("total_spent", 0)) == expected["total_spent"], f"Record {i}: Expected total_spent {expected['total_spent']}, got {actual.get('total_spent')}"
        assert int(actual.get("total_interaction_time", 0)) == expected["total_interaction_time"], f"Record {i}: Expected total_interaction_time {expected['total_interaction_time']}, got {actual.get('total_interaction_time')}"

def test_script_parameterization():
    """Test executing the script with different parameters to ensure queries are parameterized."""
    output_path = "/home/user/test_report_2.json"
    if os.path.exists(output_path):
        os.remove(output_path)

    # Execute the script with different arguments
    result = subprocess.run(
        ["/bin/bash", SCRIPT_PATH, "refunded", "100", output_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"
    assert os.path.exists(output_path), f"Output JSON file was not created at {output_path}"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} does not contain valid JSON.")

    expected_data = [
        {
            "customer_name": "Alice Smith",
            "total_spent": 50.0,
            "total_interaction_time": 120
        },
        {
            "customer_name": "Bob Jones",
            "total_spent": 0.0,
            "total_interaction_time": 300
        },
        {
            "customer_name": "Charlie Brown",
            "total_spent": 0.0,
            "total_interaction_time": 0
        }
    ]

    assert isinstance(data, list), "Output JSON must be an array of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("customer_name") == expected["customer_name"], f"Record {i}: Expected customer_name '{expected['customer_name']}', got '{actual.get('customer_name')}'"
        assert float(actual.get("total_spent", 0)) == expected["total_spent"], f"Record {i}: Expected total_spent {expected['total_spent']}, got {actual.get('total_spent')}"
        assert int(actual.get("total_interaction_time", 0)) == expected["total_interaction_time"], f"Record {i}: Expected total_interaction_time {expected['total_interaction_time']}, got {actual.get('total_interaction_time')}"