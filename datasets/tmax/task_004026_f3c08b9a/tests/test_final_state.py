# test_final_state.py

import json
import os

def test_rolling_stats_mse():
    agent_file = '/home/user/rolling_stats.json'
    reference_file = '/app/ground_truth_stats.json'

    assert os.path.exists(agent_file), f"Agent output file missing at {agent_file}"
    assert os.path.exists(reference_file), f"Reference file missing at {reference_file}"

    with open(agent_file, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Agent output at {agent_file} is not valid JSON"

    with open(reference_file, 'r') as f:
        ref_data = json.load(f)

    assert len(agent_data) > 0, "Agent output JSON array is empty"

    sq_err = 0.0
    for i in range(min(len(agent_data), len(ref_data))):
        try:
            agent_val = float(agent_data[i].get('moving_avg', 0))
        except (ValueError, TypeError):
            agent_val = 0.0

        try:
            ref_val = float(ref_data[i].get('moving_avg', 0))
        except (ValueError, TypeError):
            ref_val = 0.0

        sq_err += (agent_val - ref_val) ** 2

    # If agent data is shorter than reference, the missing elements contribute as if they were 0, 
    # but the loop above only iterates up to the min length. Let's add penalties for missing items.
    if len(agent_data) < len(ref_data):
        for i in range(len(agent_data), len(ref_data)):
            try:
                ref_val = float(ref_data[i].get('moving_avg', 0))
            except (ValueError, TypeError):
                ref_val = 0.0
            sq_err += (0.0 - ref_val) ** 2

    mse = sq_err / len(ref_data)

    threshold = 0.005
    assert mse <= threshold, f"MSE of moving_avg is {mse:.6f}, which exceeds the threshold of {threshold}"