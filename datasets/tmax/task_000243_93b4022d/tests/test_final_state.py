# test_final_state.py

import os
import json
import pytest

def test_fixed_timestamps_mse():
    output_path = "/home/user/fixed_timestamps.json"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Expected {output_path} to be a file."

    try:
        with open(output_path, "r") as f:
            agent_ts = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse JSON from {output_path}: {e}")

    duration = 5.0
    fps = 30
    expected_frames = int(duration * fps)

    assert isinstance(agent_ts, list), "Output JSON must contain a list of floats."
    assert len(agent_ts) == expected_frames, f"Expected {expected_frames} timestamps, but got {len(agent_ts)}."

    expected_ts = [i / float(fps) for i in range(expected_frames)]

    mse = sum((a - e) ** 2 for a, e in zip(agent_ts, expected_ts)) / expected_frames

    threshold = 1e-10
    assert mse <= threshold, f"MSE {mse} is greater than the allowed threshold of {threshold}."