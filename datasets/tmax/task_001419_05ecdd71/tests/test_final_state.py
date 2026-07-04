# test_final_state.py

import os
import math
import pytest

def custom_round(val):
    # Standard half-way rounding (round half up)
    return math.floor(val * 10 + 0.5) / 10.0

def process_file(filepath):
    if not os.path.exists(filepath):
        return [], {}

    raw_count = 0
    dedup_dict = {}

    with open(filepath, 'r') as f:
        lines = f.read().strip().split('\n')
        if not lines:
            return 0, {}

        # Skip header
        for line in lines[1:]:
            if not line.strip():
                continue
            raw_count += 1
            parts = line.split(',')
            if len(parts) == 4:
                pid = parts[0]
                x = custom_round(float(parts[1]))
                y = custom_round(float(parts[2]))
                z = custom_round(float(parts[3]))

                coord = (x, y, z)
                if coord not in dedup_dict:
                    dedup_dict[coord] = pid

    return raw_count, dedup_dict

def test_joined_points_csv():
    joined_path = "/home/user/joined_points.csv"
    assert os.path.isfile(joined_path), f"Output file {joined_path} does not exist."

    raw_a, dedup_a = process_file("/home/user/points_A.csv")
    raw_b, dedup_b = process_file("/home/user/points_B.csv")

    intersection = []
    for coord, id_a in dedup_a.items():
        if coord in dedup_b:
            id_b = dedup_b[coord]
            intersection.append((id_a, id_b, coord[0], coord[1], coord[2]))

    intersection.sort(key=lambda item: item[0])

    expected_lines = ["id_A,id_B,x,y,z"]
    for item in intersection:
        expected_lines.append(f"{item[0]},{item[1]},{item[2]:.1f},{item[3]:.1f},{item[4]:.1f}")

    expected_content = "\n".join(expected_lines)

    with open(joined_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {joined_path} does not match expected output.\nExpected:\n{expected_content}\nActual:\n{actual_content}"

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    raw_a, dedup_a = process_file("/home/user/points_A.csv")
    raw_b, dedup_b = process_file("/home/user/points_B.csv")

    intersect_count = sum(1 for coord in dedup_a if coord in dedup_b)

    expected_log = [
        f"Loaded {raw_a} raw points from A",
        f"Loaded {raw_b} raw points from B",
        f"Deduplicated A to {len(dedup_a)} points",
        f"Deduplicated B to {len(dedup_b)} points",
        f"Found {intersect_count} intersecting points"
    ]

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    # We only check the last 5 lines in case the user ran it multiple times, 
    # but the prompt implies appending, so let's check if the expected lines are at the end.
    assert len(actual_lines) >= 5, f"Log file {log_path} does not have enough lines."
    actual_tail = actual_lines[-5:]

    assert actual_tail == expected_log, f"Log file {log_path} content is incorrect.\nExpected tail:\n{expected_log}\nActual tail:\n{actual_tail}"