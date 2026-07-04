# test_final_state.py

import os
import json
import pytest

def test_process_graph_script_exists_and_executable():
    script_path = '/home/user/process_graph.sh'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_top_servers_json_exists_and_correct():
    output_path = '/home/user/top_servers.json'
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    expected_data = {
        "ap-south": "s5",
        "eu-west": "s3",
        "us-east": "s2"
    }

    assert data == expected_data, f"The content of {output_path} is incorrect. Expected {expected_data}, but got {data}."