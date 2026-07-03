# test_final_state.py

import os
import math
import pytest

def test_output_file_exists():
    """Test that the output.txt file exists."""
    output_path = '/home/user/output.txt'
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

def test_output_content():
    """Test that output.txt contains the correct mean and CI."""
    data_path = '/home/user/data.csv'
    output_path = '/home/user/output.txt'

    assert os.path.exists(data_path), f"Data file {data_path} is missing."

    # Recompute ground truth
    magnitudes = []
    with open(data_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) != 5:
                continue
            x_str, y_str, z_str = parts[2], parts[3], parts[4]
            if "NaN" in (x_str, y_str, z_str):
                continue
            x, y, z = float(x_str), float(y_str), float(z_str)
            mag = math.sqrt(x*x + y*y + z*z)
            magnitudes.append(mag)

    assert len(magnitudes) > 0, "No valid rows found in data.csv."

    n = len(magnitudes)
    mean = sum(magnitudes) / n
    variance = sum((m - mean)**2 for m in magnitudes) / (n - 1)
    std_dev = math.sqrt(variance)

    margin = 1.96 * (std_dev / math.sqrt(n))
    lower = mean - margin
    upper = mean + margin

    expected_output = f"Mean: {mean:.4f}, CI: [{lower:.4f}, {upper:.4f}]"

    # Read the agent's output
    with open(output_path, 'r') as f:
        agent_output = f.read().strip()

    assert agent_output == expected_output, (
        f"Output content does not match expected.\n"
        f"Expected: '{expected_output}'\n"
        f"Got: '{agent_output}'"
    )