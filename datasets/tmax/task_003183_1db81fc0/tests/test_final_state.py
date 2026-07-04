# test_final_state.py

import os
import math

def test_processed_stats_exists():
    output_file = "/home/user/processed_stats.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did the C program run successfully?"

def test_processed_stats_content():
    input_file = "/home/user/sensor_data.csv"
    output_file = "/home/user/processed_stats.csv"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."

    # Recompute the expected output from the input file
    buckets = {}
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            parts = line.split(',')
            ts = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])

            bucket = (ts // 10) * 10
            if bucket not in buckets:
                buckets[bucket] = {'x': [], 'y': []}
            buckets[bucket]['x'].append(x)
            buckets[bucket]['y'].append(y)

    sorted_buckets = sorted(buckets.keys())
    distances = []
    expected_rows = []

    for b in sorted_buckets:
        mean_x = sum(buckets[b]['x']) / len(buckets[b]['x'])
        mean_y = sum(buckets[b]['y']) / len(buckets[b]['y'])
        dist = math.sqrt(mean_x**2 + mean_y**2)
        distances.append(dist)

        window = distances[-3:]
        rolling_avg = sum(window) / len(window)

        expected_rows.append(f"{b},{dist:.2f},{rolling_avg:.2f}")

    # Read the actual output
    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) > 0, "Output file is empty."

    expected_header = "bucket_time,centroid_distance,rolling_avg_distance"
    assert actual_lines[0] == expected_header, f"Header mismatch. Expected '{expected_header}', got '{actual_lines[0]}'."

    actual_rows = actual_lines[1:]
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but found {len(actual_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_rows, actual_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected '{expected}', got '{actual}'."