# test_final_state.py
import os
import pytest

def test_test_sum_txt_exists_and_correct():
    csv_path = "/home/user/dataset_organizer/data/embeddings.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} is missing."

    # Recompute the expected value from the CSV
    with open(csv_path, 'r') as f:
        data = [[float(x) for x in line.strip().split(',')] for line in f if line.strip()]

    assert len(data) == 100, f"Expected 100 rows in CSV, found {len(data)}."

    train_set = data[:80]
    test_set = data[80:]

    num_cols = len(data[0])
    train_means = [0.0] * num_cols
    for row in train_set:
        for j in range(num_cols):
            train_means[j] += row[j]
    for j in range(num_cols):
        train_means[j] /= len(train_set)

    expected_sum = 0.0
    for row in test_set:
        for j in range(num_cols):
            expected_sum += (row[j] - train_means[j])

    expected_output = f"Test sum: {expected_sum:.4f}"

    result_path = "/home/user/dataset_organizer/test_sum.txt"
    assert os.path.isfile(result_path), f"Output file {result_path} is missing. Did you save the output?"

    with open(result_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Expected output to be '{expected_output}', but found '{actual_output}'."