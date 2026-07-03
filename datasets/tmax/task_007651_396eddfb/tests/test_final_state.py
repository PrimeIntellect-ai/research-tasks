# test_final_state.py

import os
import json
import pytest

def test_emulator_server_compiled():
    binary_path = "/home/user/emulator_release/emulator_server"
    assert os.path.isfile(binary_path), f"The binary {binary_path} was not found. Did the code compile successfully?"
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_schema_migration():
    state1_path = "/home/user/states/state_1.json"
    assert os.path.isfile(state1_path), f"The state file {state1_path} is missing."

    with open(state1_path, "r") as f:
        try:
            data1 = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {state1_path} does not contain valid JSON.")

    expected_state1 = {
        "machine_state": {
            "data_stack": [10, 20],
            "instruction_pointer": 0
        },
        "version": 2
    }
    assert data1 == expected_state1, f"The schema migration for {state1_path} is incorrect. Expected {expected_state1}, got {data1}."

    state2_path = "/home/user/states/state_2.json"
    assert os.path.isfile(state2_path), f"The state file {state2_path} is missing."

    with open(state2_path, "r") as f:
        try:
            data2 = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {state2_path} does not contain valid JSON.")

    expected_state2 = {
        "machine_state": {
            "data_stack": [5],
            "instruction_pointer": 1
        },
        "version": 2
    }
    assert data2 == expected_state2, f"The schema migration for {state2_path} is incorrect. Expected {expected_state2}, got {data2}."

def test_deployment_log():
    log_path = "/home/user/deployment_log.txt"
    assert os.path.isfile(log_path), f"The deployment log file {log_path} is missing. Did you run the curl command and save the output?"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    expected_content = "SUCCESS: Stack top is 20"
    assert log_content == expected_content, f"The deployment log content is incorrect. Expected '{expected_content}', got '{log_content}'."