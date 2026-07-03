# test_final_state.py

import os
import pytest

def test_output_files_exist():
    assert os.path.isfile("/home/user/train.csv"), "train.csv was not created."
    assert os.path.isfile("/home/user/test.csv"), "test.csv was not created."
    assert os.path.isfile("/home/user/test_log_probs.txt"), "test_log_probs.txt was not created."

def test_correct_normalization_and_split():
    embeddings_path = "/home/user/embeddings.csv"
    assert os.path.isfile(embeddings_path), "embeddings.csv is missing."

    data = []
    with open(embeddings_path, "r") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(",")
                data.append([float(parts[0]), float(parts[1]), float(parts[2]), int(parts[3])])

    assert len(data) == 100, "embeddings.csv should have 100 rows."

    # Calculate min and max strictly from the first 80 rows (training set)
    train_data = data[:80]
    mins = [min(row[i] for row in train_data) for i in range(3)]
    maxs = [max(row[i] for row in train_data) for i in range(3)]

    expected_train = []
    for row in train_data:
        norm_row = [(row[i] - mins[i]) / (maxs[i] - mins[i]) for i in range(3)]
        expected_train.append(f"{norm_row[0]:.4f},{norm_row[1]:.4f},{norm_row[2]:.4f},{row[3]}\n")

    expected_test = []
    for row in data[80:]:
        norm_row = [(row[i] - mins[i]) / (maxs[i] - mins[i]) for i in range(3)]
        expected_test.append(f"{norm_row[0]:.4f},{norm_row[1]:.4f},{norm_row[2]:.4f},{row[3]}\n")

    with open("/home/user/train.csv", "r") as f:
        actual_train = [line for line in f if line.strip()]

    with open("/home/user/test.csv", "r") as f:
        actual_test = [line for line in f if line.strip()]

    assert len(actual_train) == 80, f"train.csv should have exactly 80 rows, found {len(actual_train)}."
    assert len(actual_test) == 20, f"test.csv should have exactly 20 rows, found {len(actual_test)}."

    for i in range(80):
        assert actual_train[i] == expected_train[i], (
            f"train.csv row {i+1} is incorrect.\n"
            f"Expected: {expected_train[i].strip()}\n"
            f"Got:      {actual_train[i].strip()}\n"
            "Ensure min/max are calculated ONLY from the first 80 rows."
        )

    for i in range(20):
        assert actual_test[i] == expected_test[i], (
            f"test.csv row {i+1} is incorrect.\n"
            f"Expected: {expected_test[i].strip()}\n"
            f"Got:      {actual_test[i].strip()}\n"
            "Ensure min/max are calculated ONLY from the first 80 rows and applied to all 100 rows."
        )

def test_log_probs_output():
    log_probs_path = "/home/user/test_log_probs.txt"
    assert os.path.isfile(log_probs_path), "test_log_probs.txt is missing."

    with open(log_probs_path, "r") as f:
        lines = [line for line in f if line.strip()]

    assert len(lines) == 20, f"test_log_probs.txt should have 20 rows, found {len(lines)}."

    for i, line in enumerate(lines):
        parts = line.strip().split(",")
        assert len(parts) == 2, f"test_log_probs.txt row {i+1} should have 2 columns (log-probs for class 0 and 1)."
        try:
            float(parts[0])
            float(parts[1])
        except ValueError:
            pytest.fail(f"test_log_probs.txt row {i+1} contains non-numeric values: {line.strip()}")