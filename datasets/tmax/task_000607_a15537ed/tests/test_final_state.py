# test_final_state.py

import os
import subprocess
import re
import pytest
import json

def test_merged_timeline_exists():
    path = "/home/user/log_pipeline/merged_timeline.json"
    assert os.path.isfile(path), f"Expected output file {path} is missing. Did you run the script and save the output correctly?"

def test_merged_timeline_valid_json():
    path = "/home/user/log_pipeline/merged_timeline.json"
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        assert isinstance(data, list), "The JSON file must contain an array of objects."
    except json.JSONDecodeError:
        pytest.fail(f"The file {path} does not contain valid JSON.")

def test_score_timeline_metric():
    agent_file_path = "/home/user/log_pipeline/merged_timeline.json"
    binary_path = "/app/score_timeline"

    assert os.path.isfile(binary_path), f"Evaluation binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Evaluation binary {binary_path} is not executable."

    try:
        result = subprocess.run(
            [binary_path, agent_file_path], 
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The evaluation binary timed out. Check your JSON file for extreme sizes or formatting issues.")
    except Exception as e:
        pytest.fail(f"Failed to execute the evaluation binary: {e}")

    match = re.search(r'SCORE:\s*([\d\.]+)', result.stdout)
    assert match is not None, f"Could not parse SCORE from binary output. Output was: {result.stdout}"

    score = float(match.group(1))
    assert score >= 95.0, f"Score {score} is less than the required threshold of 95.0."