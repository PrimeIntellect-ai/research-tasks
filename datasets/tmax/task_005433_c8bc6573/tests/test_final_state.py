# test_final_state.py
import json
import os

def test_metrics_accuracy():
    agent_file = '/home/user/final_metrics.json'
    reference_file = '/tmp/reference_metrics.json'

    assert os.path.isfile(agent_file), f"Agent output file {agent_file} is missing."
    assert os.path.isfile(reference_file), f"Reference file {reference_file} is missing."

    with open(agent_file, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Failed to parse JSON from {agent_file}."

    with open(reference_file, 'r') as f:
        ref_data = json.load(f)

    assert len(agent_data) == len(ref_data), f"Frame count mismatch: agent has {len(agent_data)}, expected {len(ref_data)}."

    agent_dict = {item['frame']: item['brightness'] for item in agent_data}
    ref_dict = {item['frame']: item['brightness'] for item in ref_data}

    # Ensure all frames from reference are present in agent output
    missing_frames = set(ref_dict.keys()) - set(agent_dict.keys())
    assert not missing_frames, f"Agent output is missing frames: {missing_frames}"

    mse = sum((agent_dict[k] - ref_dict[k])**2 for k in ref_dict) / len(ref_dict)

    assert mse <= 2.0, f"MSE {mse:.4f} exceeds the threshold of 2.0"