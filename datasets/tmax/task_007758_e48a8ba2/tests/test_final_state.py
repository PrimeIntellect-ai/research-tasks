# test_final_state.py

import os
import struct
from collections import defaultdict

def test_output_exists():
    """Test that the output CSV file exists."""
    path = "/home/user/output.csv"
    assert os.path.exists(path), f"Output file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.path.getsize(path) > 0, f"{path} is empty."

def test_output_content():
    """Test that the output CSV contains the correct rolling averages and ordering."""
    csv_path = "/home/user/data.csv"
    bin_path = "/home/user/data.bin"
    output_path = "/home/user/output.csv"

    # Check if inputs exist just in case
    assert os.path.exists(csv_path), f"Input file {csv_path} is missing."
    assert os.path.exists(bin_path), f"Input file {bin_path} is missing."

    records = []

    # Read CSV
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, ts, val = line.split(',')
            records.append((int(sid), int(ts), float(val)))

    # Read BIN
    with open(bin_path, 'rb') as f:
        while True:
            chunk = f.read(20)
            if not chunk:
                break
            sid, ts, val = struct.unpack('<iqd', chunk)
            records.append((sid, ts, val))

    # Sort records by timestamp, then sensor_id
    records.sort(key=lambda x: (x[1], x[0]))

    # Compute expected output
    hist = defaultdict(list)
    expected_output = []
    for r in records:
        sid, ts, val = r
        hist[sid].append(val)
        if len(hist[sid]) > 3:
            hist[sid].pop(0)
        avg = sum(hist[sid]) / len(hist[sid])
        expected_output.append(f"{sid},{ts},{avg:.4f}")

    # Read actual output
    actual_output = []
    with open(output_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                actual_output.append(line)

    # Compare
    assert len(actual_output) == len(expected_output), f"Output record count mismatch. Expected {len(expected_output)}, got {len(actual_output)}."

    for i, (expected, actual) in enumerate(zip(expected_output, actual_output)):
        assert actual == expected, f"Mismatch at line {i+1}. Expected '{expected}', got '{actual}'."