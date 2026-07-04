# test_final_state.py

import os
import struct
import math
import pandas as pd

def test_telemetry_bin_rmse():
    """Test that the telemetry.bin file exists, has the correct number of frames, and its RMSE is < 2.0."""
    bin_path = '/home/user/telemetry.bin'
    gt_path = '/tmp/gt.csv'

    assert os.path.exists(bin_path), f"Agent output file {bin_path} does not exist."
    assert os.path.exists(gt_path), f"Ground truth file {gt_path} is missing."

    gt = pd.read_csv(gt_path)

    agent_data = []
    with open(bin_path, 'rb') as f:
        while chunk := f.read(12):
            if len(chunk) == 12:
                frame, x, y = struct.unpack('iff', chunk)
                agent_data.append({'frame': frame, 'x': x, 'y': y})

    assert len(agent_data) == len(gt), f"Expected {len(gt)} frames in telemetry.bin, got {len(agent_data)}."

    sq_err = 0
    for i in range(len(gt)):
        sq_err += (gt.iloc[i]['x'] - agent_data[i]['x'])**2
        sq_err += (gt.iloc[i]['y'] - agent_data[i]['y'])**2

    rmse = math.sqrt(sq_err / (2 * len(gt)))

    assert rmse < 2.0, f"Calculated RMSE={rmse} is not less than the required threshold of 2.0."

def test_stats_csv_format():
    """Test that stats.csv exists and contains exactly 3 comma-separated numerical values."""
    stats_path = '/home/user/stats.csv'
    assert os.path.exists(stats_path), f"Agent output file {stats_path} does not exist."

    with open(stats_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 3, f"Expected exactly 3 comma-separated values in stats.csv, got {len(parts)}. Content: '{content}'"

    for i, part in enumerate(parts):
        try:
            float(part)
        except ValueError:
            assert False, f"Value at index {i} ('{part}') in stats.csv is not a valid float."