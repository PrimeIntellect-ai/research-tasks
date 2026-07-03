# test_final_state.py
import json
import os
import pytest

def test_energy_totals_mae():
    json_path = '/home/user/energy_totals.json'
    assert os.path.isfile(json_path), f"Output file missing: {json_path}"

    try:
        with open(json_path, 'r') as f:
            agent_data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load JSON from {json_path}: {e}")

    truth = {
        "ALPH": 420.0,
        "BETA": 720.0,
        "GAMM": 820.0
    }

    mae = 0.0
    count = len(truth)

    for node, expected_val in truth.items():
        agent_val = agent_data.get(node, 0.0)
        try:
            agent_val = float(agent_val)
        except (ValueError, TypeError):
            agent_val = 0.0
        mae += abs(expected_val - agent_val)

    mae = mae / count

    assert mae <= 50.0, f"MAE is {mae}, which is greater than the threshold of 50.0"