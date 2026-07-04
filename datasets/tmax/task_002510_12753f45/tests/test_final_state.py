# test_final_state.py

import os
import subprocess
import re
import pytest

def get_loss(binary_path, data_path):
    out = subprocess.check_output([binary_path, data_path], text=True)
    match = re.search(r"Final loss:\s*([0-9]+\.[0-9]+)", out)
    if not match:
        return float('inf')
    return float(match.group(1))

def test_fixed_binary_exists_and_executable():
    path = "/home/user/optimized_engine_fixed"
    assert os.path.isfile(path), f"Fixed binary not found at {path}"
    assert os.access(path, os.X_OK), f"Fixed binary at {path} is not executable"

def test_fixed_binary_loss_metric():
    oracle_path = '/app/oracle_bin'
    agent_path = '/home/user/optimized_engine_fixed'
    data_path = '/app/secret_test_data.csv'

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.path.isfile(data_path), f"Secret test data not found at {data_path}"

    try:
        oracle_loss = get_loss(oracle_path, data_path)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle binary failed to execute: {e}")

    try:
        agent_loss = get_loss(agent_path, data_path)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent binary failed to execute: {e}")

    assert agent_loss != float('inf'), "Agent binary output did not match the expected format 'Final loss: <float>'"
    assert oracle_loss != float('inf'), "Oracle binary output did not match the expected format 'Final loss: <float>'"

    error = abs(oracle_loss - agent_loss)
    threshold = 1e-4

    assert error <= threshold, f"Loss error {error} exceeds threshold {threshold}. Agent loss: {agent_loss}, Oracle loss: {oracle_loss}"