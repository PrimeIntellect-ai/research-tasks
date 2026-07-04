# test_final_state.py

import os
import json

def test_debug_results_exists_and_correct():
    """Check if debug_results.txt exists and contains the correct findings."""
    file_path = "/home/user/log_pipeline/debug_results.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]

    expected_hang_line = "HANG_LINE=3142"
    expected_ip = "ANOMALOUS_IP=10.0.0.99"

    assert expected_hang_line in lines, f"Could not find '{expected_hang_line}' in {file_path}. Content was: {content}"
    assert expected_ip in lines, f"Could not find '{expected_ip}' in {file_path}. Content was: {content}"

def test_parsed_logs_json_exists_and_valid():
    """Check if parsed_logs.json was generated and is valid JSON."""
    file_path = "/home/user/log_pipeline/parsed_logs.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The script might not have completed successfully."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"{file_path} is not a valid JSON file. Error: {e}"

    assert isinstance(data, list), f"Expected the parsed JSON to be a list, but got {type(data).__name__}."
    assert len(data) > 0, "The parsed JSON list is empty, but it should contain log entries."