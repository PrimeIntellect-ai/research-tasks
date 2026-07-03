# test_final_state.py

import os
import glob
import pytest

def test_ca_coords_extracted_correctly():
    pdb_path = "/home/user/data/protein.pdb"
    ca_coords_path = "/home/user/ca_coords.txt"

    assert os.path.exists(ca_coords_path), f"File {ca_coords_path} is missing."

    expected_coords = []
    if os.path.exists(pdb_path):
        with open(pdb_path, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 8 and parts[0] == "ATOM" and parts[2] == "CA":
                    expected_coords.append(f"{parts[5]} {parts[6]} {parts[7]}")

    with open(ca_coords_path, "r") as f:
        actual_coords = [line.strip() for line in f if line.strip()]

    assert actual_coords == expected_coords, f"Contents of {ca_coords_path} do not match the expected CA coordinates."

def test_reduce_script_fixed():
    reduce_path = "/home/user/reduce.sh"
    assert os.path.exists(reduce_path), f"File {reduce_path} is missing."

    with open(reduce_path, "r") as f:
        content = f.read()

    assert "sort" in content and "-n" in content, "reduce.sh does not appear to sort the values numerically (missing 'sort -n' or equivalent)."
    assert "awk" in content, "reduce.sh is missing 'awk' for summation."

def test_final_sum_correct():
    results_dir = "/home/user/results"
    final_sum_path = "/home/user/final_sum.txt"

    assert os.path.exists(final_sum_path), f"File {final_sum_path} is missing."

    score_files = glob.glob(os.path.join(results_dir, "*.score"))
    assert len(score_files) > 0, "No .score files found in /home/user/results."

    scores = []
    for sf in score_files:
        with open(sf, "r") as f:
            val = f.read().strip()
            if val:
                scores.append(float(val))

    # Replicate the required sorting and reduction logic
    scores.sort()
    expected_sum = 0.0
    for s in scores:
        expected_sum += s

    expected_sum_str = f"{expected_sum:.15f}"

    with open(final_sum_path, "r") as f:
        actual_sum_str = f.read().strip()

    assert actual_sum_str == expected_sum_str, f"Final sum in {final_sum_path} ({actual_sum_str}) does not match expected sorted sum ({expected_sum_str})."

def test_histogram_correct():
    results_dir = "/home/user/results"
    histogram_path = "/home/user/histogram.txt"

    assert os.path.exists(histogram_path), f"File {histogram_path} is missing."

    score_files = glob.glob(os.path.join(results_dir, "*.score"))

    scores = []
    for sf in score_files:
        with open(sf, "r") as f:
            val = f.read().strip()
            if val:
                scores.append(float(val))

    bin1 = sum(1 for x in scores if x < 0.0)
    bin2 = sum(1 for x in scores if 0.0 <= x < 10.0)
    bin3 = sum(1 for x in scores if 10.0 <= x < 100.0)
    bin4 = sum(1 for x in scores if x >= 100.0)

    expected_histogram = {
        "bin1_lt_0": bin1,
        "bin2_0_10": bin2,
        "bin3_10_100": bin3,
        "bin4_ge_100": bin4
    }

    actual_histogram = {}
    with open(histogram_path, "r") as f:
        for line in f:
            if ":" in line:
                key, val = line.split(":", 1)
                actual_histogram[key.strip()] = int(val.strip())

    for key, expected_count in expected_histogram.items():
        assert key in actual_histogram, f"Missing key {key} in {histogram_path}."
        assert actual_histogram[key] == expected_count, f"Count for {key} in {histogram_path} is {actual_histogram[key]}, expected {expected_count}."