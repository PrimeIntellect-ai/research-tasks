# test_final_state.py

import os
import json
import pytest

def test_process_configs_script_exists():
    """Verify that the Python script was created."""
    script_path = "/home/user/process_configs.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_hourly_summary_json():
    """Verify that the hourly summary JSON is correctly generated."""
    json_path = "/home/user/hourly_summary.json"
    assert os.path.exists(json_path), f"The output file {json_path} does not exist. Did you run your script?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_data = {
        "2023-10-24 14": [
            "feature_flag_x=true",
            "max_connections=500",
            "timeout=30"
        ],
        "2023-10-24 15": [
            "feature_flag_x=false",
            "max_connections=600",
            "timeout=30"
        ]
    }

    assert data == expected_data, f"The content of {json_path} does not match the expected output."

def test_pipeline_log():
    """Verify that the pipeline log is correctly generated."""
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"The output file {log_path} does not exist. Did you run your script?"

    with open(log_path, 'r') as f:
        log_content = f.read().strip()

    expected_log = "Processed 8 lines successfully."
    assert log_content == expected_log, f"The content of {log_path} is incorrect. Expected '{expected_log}', got '{log_content}'."