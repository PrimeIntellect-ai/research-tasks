# test_final_state.py
import os
import pytest

def test_centralities_mse():
    output_path = "/home/user/centralities.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    expected = {
        "A": 0.1481,
        "B": 0.3077,
        "C": 0.2667,
        "D": 0.2500,
        "E": 0.1739
    }

    try:
        with open(output_path, "r") as f:
            lines = f.read().strip().split('\n')

        agent_vals = {}
        for line in lines:
            if ":" in line:
                parts = line.split(":")
                node = parts[0].strip()
                val = float(parts[1].strip())
                agent_vals[node] = val

        mse = 0.0
        for k, v in expected.items():
            if k in agent_vals:
                mse += (agent_vals[k] - v) ** 2
            else:
                mse += 1.0 # High penalty for missing nodes

        mse /= len(expected)
    except Exception as e:
        pytest.fail(f"Failed to parse {output_path}: {e}")

    threshold = 0.001
    assert mse <= threshold, f"MSE {mse} exceeds the maximum allowed threshold of {threshold}."