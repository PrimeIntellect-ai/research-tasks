# test_final_state.py

import os
import math
import csv
from itertools import combinations

def test_closest_pair_result():
    output_file = "/home/user/closest_pair.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    metadata_file = "/home/user/data/metadata.csv"
    series_file = "/home/user/data/series.csv"

    assert os.path.isfile(metadata_file), "metadata.csv is missing."
    assert os.path.isfile(series_file), "series.csv is missing."

    # 1. Read metadata
    target_exps = set()
    with open(metadata_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Category'] == 'Target':
                target_exps.add(row['ExpID'])

    # 2. Read and process series
    cleaned_data = {}
    with open(series_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            exp_id = row[0]
            if exp_id not in target_exps:
                continue

            raw_vals = row[1:6]
            present_capped = []

            # Cap outliers
            for v in raw_vals:
                if v.strip():
                    val = float(v)
                    if val > 100.0:
                        val = 100.0
                    elif val < 0.0:
                        val = 0.0
                    present_capped.append(val)

            # Compute mean
            mean_val = sum(present_capped) / len(present_capped) if present_capped else 0.0

            # Fill missing
            final_vals = []
            for v in raw_vals:
                if v.strip():
                    val = float(v)
                    if val > 100.0:
                        val = 100.0
                    elif val < 0.0:
                        val = 0.0
                    final_vals.append(val)
                else:
                    final_vals.append(mean_val)

            cleaned_data[exp_id] = final_vals

    # 3. Calculate distances
    min_dist = float('inf')
    best_pair = None

    for expA, expB in combinations(sorted(cleaned_data.keys()), 2):
        vecA = cleaned_data[expA]
        vecB = cleaned_data[expB]
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(vecA, vecB)))

        if dist < min_dist:
            min_dist = dist
            best_pair = (expA, expB)

    expected_expA, expected_expB = sorted(best_pair)
    expected_distance_str = f"{min_dist:.4f}"
    expected_output = f"{expected_expA},{expected_expB},{expected_distance_str}"

    # 4. Read student output
    with open(output_file, 'r') as f:
        student_output = f.read().strip()

    assert student_output == expected_output, (
        f"Output in {output_file} does not match expected.\n"
        f"Expected: '{expected_output}'\n"
        f"Got: '{student_output}'"
    )