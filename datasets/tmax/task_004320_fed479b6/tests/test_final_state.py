# test_final_state.py

import os
import csv
import math
import re
import pytest

def compute_expected_features(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        data = {col: [] for col in reader.fieldnames}
        for row in reader:
            for col in reader.fieldnames:
                data[col].append(float(row[col]))

    target = data['Target']
    n = len(target)
    mean_t = sum(target) / n
    var_t = sum((t - mean_t)**2 for t in target)

    corrs = {}
    for col in ['F1', 'F2', 'F3', 'F4', 'F5']:
        x = data[col]
        mean_x = sum(x) / n
        cov = sum((x[i] - mean_x) * (target[i] - mean_t) for i in range(n))
        var_x = sum((xi - mean_x)**2 for xi in x)
        corr = cov / math.sqrt(var_x * var_t)
        corrs[col] = abs(corr)

    # Get top 2 features by absolute correlation
    sorted_features = sorted(corrs.keys(), key=lambda k: corrs[k], reverse=True)
    top_2 = sorted(sorted_features[:2])
    return top_2

def test_etl_output_exists():
    output_path = '/home/user/etl_output.txt'
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

def test_etl_output_content():
    output_path = '/home/user/etl_output.txt'
    csv_path = '/home/user/sensor_data.csv'

    assert os.path.exists(output_path), "Output file missing."
    assert os.path.exists(csv_path), "Input CSV missing."

    expected_features = compute_expected_features(csv_path)
    expected_line1 = f"{expected_features[0]},{expected_features[1]}"

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, "Output file must contain at least two lines."

    # Check Line 1
    assert lines[0] == expected_line1, f"Expected line 1 to be '{expected_line1}', got '{lines[0]}'."

    # Check Line 2
    line2 = lines[1]
    assert re.match(r'^-?\d+\.\d{4}$', line2), f"Expected line 2 to be a float rounded to exactly 4 decimal places, got '{line2}'."

    coef = float(line2)
    # The expected coefficient is around 0.4905. We allow a reasonable range to account for numpy random sampling variations
    # if different numpy versions are used, but it should be structurally close.
    assert 0.40 <= coef <= 0.60, f"Expected bootstrap mean coefficient to be around 0.49, got {coef}."