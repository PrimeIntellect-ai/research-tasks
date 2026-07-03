# test_final_state.py

import os
import pytest

TARGET_VALUE = 0.0452918
THRESHOLD = 1e-5
OUTPUT_FILE = "/home/user/posterior_mean.txt"

def test_posterior_mean_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Expected output file {OUTPUT_FILE} does not exist."

def test_posterior_mean_value():
    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()

    assert content, f"File {OUTPUT_FILE} is empty."

    try:
        agent_value = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {OUTPUT_FILE} as a float. Content: '{content}'")

    error = abs(agent_value - TARGET_VALUE)
    assert error <= THRESHOLD, (
        f"Posterior mean absolute error is too high. "
        f"Agent value: {agent_value}, Target: {TARGET_VALUE}, "
        f"Error: {error}, Threshold: {THRESHOLD}"
    )