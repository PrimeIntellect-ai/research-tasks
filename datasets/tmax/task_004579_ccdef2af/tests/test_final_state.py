# test_final_state.py
import json
import os
import pytest

def test_output_json_exists():
    output_path = '/home/user/output.json'
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_mse_metric():
    agent_file = '/home/user/output.json'
    truth_file = '/app/truth.json'

    assert os.path.exists(agent_file), f"Agent file missing: {agent_file}"
    assert os.path.exists(truth_file), f"Truth file missing: {truth_file}"

    with open(agent_file, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {agent_file} as JSON.")

    with open(truth_file, 'r') as f:
        truth_data = json.load(f)

    assert isinstance(agent_data, list), "Agent output should be a JSON list."
    assert len(agent_data) == len(truth_data), f"Length mismatch: agent has {len(agent_data)} frames, truth has {len(truth_data)} frames."

    for i, a in enumerate(agent_data):
        assert 'score' in a, f"Frame {i} in agent output is missing the 'score' key."

    mse = sum((a['score'] - t['score'])**2 for a, t in zip(agent_data, truth_data)) / len(agent_data)

    threshold = 0.01
    assert mse <= threshold, f"MSE {mse:.6f} is greater than the threshold {threshold}."