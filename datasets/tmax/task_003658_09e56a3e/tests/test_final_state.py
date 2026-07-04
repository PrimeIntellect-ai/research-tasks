# test_final_state.py

import os
import json
import subprocess
import time
import pytest

def test_files_exist():
    script_path = "/home/user/query_datasets.py"
    results_path = "/home/user/results.json"

    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(results_path), f"The results file {results_path} does not exist."

def test_jaccard_similarity():
    results_path = "/home/user/results.json"
    oracle_path = "/app/dataset_oracle"

    assert os.path.isfile(results_path), f"The results file {results_path} does not exist."
    assert os.path.isfile(oracle_path), f"The oracle binary {oracle_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            agent_data = json.load(f)
            agent_out = set(agent_data)
        except json.JSONDecodeError:
            pytest.fail("The results file is not valid JSON.")

    try:
        oracle_output = subprocess.check_output([oracle_path, 'root_001', '2']).decode('utf-8')
        oracle_out = set(json.loads(oracle_output))
    except Exception as e:
        pytest.fail(f"Failed to execute oracle binary or parse its output: {e}")

    intersection = len(agent_out.intersection(oracle_out))
    union = len(agent_out.union(oracle_out))
    jaccard = intersection / union if union > 0 else 1.0

    assert jaccard >= 1.0, f"Jaccard similarity is {jaccard}, expected >= 1.0. Agent out: {agent_out}, Oracle out: {oracle_out}"

def test_execution_time():
    script_path = "/home/user/query_datasets.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    start_time = time.time()
    try:
        subprocess.check_output(['python3', script_path, 'root_001', '2'])
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed: {e}")
    end_time = time.time()

    execution_time = end_time - start_time
    assert execution_time < 0.1, f"Execution time was {execution_time:.3f} seconds, which exceeds the 0.1s threshold."