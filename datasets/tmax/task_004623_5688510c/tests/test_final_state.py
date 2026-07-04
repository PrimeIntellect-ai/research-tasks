# test_final_state.py
import os
import csv
import math
import pytest

def compute_truth():
    dataset_path = "/home/user/dataset.csv"
    if not os.path.exists(dataset_path):
        pytest.fail(f"Dataset missing at {dataset_path}")

    data = []
    with open(dataset_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'id': int(row['ID']),
                'a': float(row['Feature_A']),
                'b': float(row['Feature_B']),
                'c': float(row['Feature_C']),
                'target': float(row['Target'])
            })

    n = len(data)
    if n == 0:
        pytest.fail("Dataset is empty.")

    def pearson(x_key, y_key):
        sum_x = sum(d[x_key] for d in data)
        sum_y = sum(d[y_key] for d in data)
        sum_x2 = sum(d[x_key]**2 for d in data)
        sum_y2 = sum(d[y_key]**2 for d in data)
        sum_xy = sum(d[x_key]*d[y_key] for d in data)

        num = n * sum_xy - sum_x * sum_y
        den = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
        return num / den

    cor_a = pearson('a', 'target')
    cor_b = pearson('b', 'target')
    cor_c = pearson('c', 'target')

    qA, qB, qC = 5.0, 3.0, 1.0
    for d in data:
        d['dist'] = math.sqrt((d['a']-qA)**2 + (d['b']-qB)**2 + (d['c']-qC)**2)

    sorted_data = sorted(data, key=lambda x: x['dist'])
    top3_ids = [d['id'] for d in sorted_data[:3]]

    return cor_a, cor_b, cor_c, top3_ids

def test_results_file_exists():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"The output file {results_path} was not found. Did you run the program and redirect output?"

def test_results_content_correct():
    results_path = "/home/user/results.txt"
    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, f"The file {results_path} should contain at least 2 lines of output."

    cor_a, cor_b, cor_c, top3_ids = compute_truth()

    expected_line1 = f"Correlations: Feature_A:{cor_a:.4f}, Feature_B:{cor_b:.4f}, Feature_C:{cor_c:.4f}"
    expected_line2 = f"Top 3 Similar IDs: {top3_ids[0]}, {top3_ids[1]}, {top3_ids[2]}"

    assert lines[0] == expected_line1, f"Line 1 mismatch.\nExpected: '{expected_line1}'\nFound:    '{lines[0]}'"
    assert lines[1] == expected_line2, f"Line 2 mismatch.\nExpected: '{expected_line2}'\nFound:    '{lines[1]}'"