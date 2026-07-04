# test_final_state.py

import os
import math
import pytest

def get_expected_result():
    dataset_path = "/home/user/data/dataset.csv"
    if not os.path.exists(dataset_path):
        pytest.fail(f"Dataset missing at {dataset_path}")

    with open(dataset_path, "r") as f:
        lines = f.read().strip().split('\n')

    data = []
    for line in lines:
        if not line:
            continue
        parts = line.split(',')
        data.append((float(parts[0]), float(parts[1])))

    train_data = data[:8]
    test_data = data[8:]

    # Compute min and max strictly on training set
    min_f1 = min(row[0] for row in train_data)
    max_f1 = max(row[0] for row in train_data)
    min_f2 = min(row[1] for row in train_data)
    max_f2 = max(row[1] for row in train_data)

    # Scale data
    def scale(row):
        return (
            (row[0] - min_f1) / (max_f1 - min_f1),
            (row[1] - min_f2) / (max_f2 - min_f2)
        )

    scaled_train = [scale(row) for row in train_data]
    scaled_test = [scale(row) for row in test_data]

    target_test_sample = scaled_test[0]

    # Find nearest neighbor in train set
    min_dist = float('inf')
    best_idx = -1

    for i, train_sample in enumerate(scaled_train):
        dist = math.sqrt((target_test_sample[0] - train_sample[0])**2 + (target_test_sample[1] - train_sample[1])**2)
        if dist < min_dist:
            min_dist = dist
            best_idx = i

    return f"{best_idx},{min_dist:.4f}"

def test_nearest_neighbor_output():
    output_path = "/home/user/nearest_neighbor.txt"
    assert os.path.isfile(output_path), f"Output file is missing: {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = get_expected_result()

    assert content == expected_content, f"Expected output '{expected_content}', but got '{content}'"