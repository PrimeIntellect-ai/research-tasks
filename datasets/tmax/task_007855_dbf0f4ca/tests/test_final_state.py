# test_final_state.py

import os
import json
import pytest

RESULT_FILE = '/home/user/result.json'

def test_result_file_exists():
    """Check if the result.json file exists."""
    assert os.path.isfile(RESULT_FILE), f"{RESULT_FILE} does not exist."

def test_result_format():
    """Check if result.json is valid JSON and contains the required key."""
    with open(RESULT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_FILE} does not contain valid JSON.")

    assert isinstance(data, dict), f"JSON in {RESULT_FILE} should be an object/dictionary."
    assert 'alpha' in data, f"'alpha' key is missing from {RESULT_FILE}."
    assert isinstance(data['alpha'], (int, float)), "'alpha' value should be a number."

def test_alpha_value():
    """Check if the calculated alpha value is correct."""
    with open(RESULT_FILE, 'r') as f:
        data = json.load(f)

    agent_alpha = data.get('alpha')
    # The expected alpha is computed from the deterministic setup using np.random.seed(42)
    # expected_alpha = 0.6508
    expected_alpha = 0.6508

    assert abs(agent_alpha - expected_alpha) <= 0.0001, (
        f"The calculated alpha value is incorrect. Expected {expected_alpha}, got {agent_alpha}."
    )