# test_final_state.py

import os
import math
import pytest

def compute_expected_values():
    total_energy = 0.0
    csv_lines = ["graph_id,energy"]

    for i in range(100):
        filepath = f'/home/user/data/graph_{i}.txt'
        degrees = {}
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    u, v = map(int, line.split(','))
                    degrees[u] = degrees.get(u, 0) + 1
                    degrees[v] = degrees.get(v, 0) + 1

        energy = sum(deg * math.sin(v + 1.2345) for v, deg in degrees.items())
        csv_lines.append(f"{i},{energy:.8f}")
        total_energy += energy

    expected_total_energy_str = f"{total_energy:.8f}"
    return expected_total_energy_str, csv_lines

def test_total_energy_file():
    total_energy_file = "/home/user/total_energy.txt"
    assert os.path.exists(total_energy_file), f"File {total_energy_file} is missing."

    expected_total_energy_str, _ = compute_expected_values()

    with open(total_energy_file, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_total_energy_str, (
        f"Total energy in {total_energy_file} is incorrect. "
        f"Expected '{expected_total_energy_str}', got '{actual_content}'."
    )

def test_features_csv_file():
    features_csv_file = "/home/user/features.csv"
    assert os.path.exists(features_csv_file), f"File {features_csv_file} is missing."

    _, expected_csv_lines = compute_expected_values()

    with open(features_csv_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_csv_lines), (
        f"Incorrect number of lines in {features_csv_file}. "
        f"Expected {len(expected_csv_lines)}, got {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_csv_lines)):
        assert actual == expected, (
            f"Mismatch in {features_csv_file} at line {i + 1}. "
            f"Expected '{expected}', got '{actual}'."
        )