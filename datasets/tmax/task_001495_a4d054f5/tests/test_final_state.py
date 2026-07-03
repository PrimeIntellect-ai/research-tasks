# test_final_state.py

import os
import json
import pytest

def test_token_file():
    token_path = "/home/user/token.txt"
    assert os.path.isfile(token_path), f"File {token_path} is missing."

    with open(token_path, "r") as f:
        content = f.read().strip()

    expected_token = "super_secret_devops_token_99"
    assert content == expected_token, f"Token in {token_path} is incorrect. Expected '{expected_token}', got '{content}'."

def test_converged_state_file():
    state_path = "/home/user/converged_state.json"
    assert os.path.isfile(state_path), f"File {state_path} is missing."

    with open(state_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {state_path} does not contain valid JSON.")

    expected_state = {
        "debug_mode": "true",
        "worker_threads": "4"
    }

    assert data == expected_state, f"State in {state_path} is incorrect. Expected {expected_state}, got {data}."