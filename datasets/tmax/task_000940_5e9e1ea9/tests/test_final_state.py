# test_final_state.py

import os
import math

def test_train_csv_created():
    """Verify train.csv exists and has exactly 100 lines."""
    assert os.path.isfile("/home/user/train.csv"), "/home/user/train.csv is missing"
    with open("/home/user/train.csv", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 100, f"Expected 100 lines in train.csv, found {len(lines)}"

def test_test_csv_created():
    """Verify test.csv exists and has exactly 40 lines."""
    assert os.path.isfile("/home/user/test.csv"), "/home/user/test.csv is missing"
    with open("/home/user/test.csv", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 40, f"Expected 40 lines in test.csv, found {len(lines)}"

def test_executable_exists():
    """Verify the C program was compiled to /home/user/pipeline."""
    assert os.path.isfile("/home/user/pipeline"), "/home/user/pipeline executable is missing"
    assert os.access("/home/user/pipeline", os.X_OK), "/home/user/pipeline is not executable"

def test_predictions_correct():
    """Verify the predictions in test_predictions.txt match the expected output."""
    assert os.path.isfile("/home/user/test_predictions.txt"), "/home/user/test_predictions.txt is missing"

    # Read the data from the files
    train_data = []
    with open("/home/user/train.csv", "r") as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            train_data.append([float(parts[0]), float(parts[1]), float(parts[2])])

    test_data = []
    with open("/home/user/test.csv", "r") as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            test_data.append([float(parts[0]), float(parts[1]), float(parts[2])])

    # Calculate means on train_data
    num_train = len(train_data)
    means = [0.0, 0.0, 0.0]
    for row in train_data:
        for j in range(3):
            means[j] += row[j]
    for j in range(3):
        means[j] /= num_train

    # Calculate stds on train_data
    stds = [0.0, 0.0, 0.0]
    for row in train_data:
        for j in range(3):
            stds[j] += (row[j] - means[j]) ** 2
    for j in range(3):
        stds[j] = math.sqrt(stds[j] / num_train)
        if stds[j] == 0:
            stds[j] = 1.0

    # Calculate predictions on test_data
    weights = [0.5, -1.2, 0.8]
    bias = 2.0
    expected_predictions = []

    for row in test_data:
        pred = bias
        for j in range(3):
            norm_val = (row[j] - means[j]) / stds[j]
            pred += norm_val * weights[j]
        expected_predictions.append(f"{pred:.4f}")

    # Read actual predictions
    with open("/home/user/test_predictions.txt", "r") as f:
        actual_predictions = [line.strip() for line in f if line.strip()]

    assert len(actual_predictions) == len(expected_predictions), \
        f"Expected {len(expected_predictions)} predictions, found {len(actual_predictions)}"

    for i, (actual, expected) in enumerate(zip(actual_predictions, expected_predictions)):
        assert actual == expected, \
            f"Prediction mismatch at line {i+1}: expected {expected}, got {actual}. The data leak may not be fully fixed."