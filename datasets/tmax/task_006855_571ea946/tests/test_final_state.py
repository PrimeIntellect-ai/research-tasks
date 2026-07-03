# test_final_state.py
import os
import struct
import math
import pytest

def test_predictions_output():
    preds_path = "/home/user/test_predictions.txt"
    assert os.path.isfile(preds_path), f"File {preds_path} is missing. Did you compile and run the program?"

    data_path = "/home/user/dataset.bin"
    assert os.path.isfile(data_path), f"File {data_path} is missing."

    # Read the binary dataset
    data = []
    with open(data_path, 'rb') as f:
        for _ in range(12000):
            row = []
            for _ in range(5):
                b = f.read(4)
                if not b:
                    break
                row.append(struct.unpack('f', b)[0])
            if len(row) == 5:
                data.append(row)

    assert len(data) == 12000, f"Expected 12000 samples in dataset.bin, got {len(data)}"

    train_size = 10000
    num_features = 5

    # Compute training statistics (mean and population stddev)
    means = [0.0] * num_features
    for i in range(train_size):
        for j in range(num_features):
            means[j] += data[i][j]
    for j in range(num_features):
        means[j] /= train_size

    stddevs = [0.0] * num_features
    for i in range(train_size):
        for j in range(num_features):
            stddevs[j] += (data[i][j] - means[j]) ** 2
    for j in range(num_features):
        stddevs[j] = math.sqrt(stddevs[j] / train_size)

    # Compute expected predictions for the test set
    weights = [0.5, -0.2, 0.1, 0.8, -0.5]
    bias = 0.1

    expected_preds = []
    for i in range(train_size, 12000):
        pred = bias
        for j in range(num_features):
            norm_val = (data[i][j] - means[j]) / stddevs[j]
            pred += norm_val * weights[j]
        expected_preds.append(pred)

    # Read the actual predictions
    with open(preds_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 2000, f"Expected exactly 2000 predictions in {preds_path}, but got {len(actual_lines)}. Ensure you only output predictions for the test set."

    # Verify each prediction
    for idx, (expected, actual) in enumerate(zip(expected_preds, actual_lines)):
        try:
            actual_val = float(actual)
        except ValueError:
            pytest.fail(f"Line {idx+1} in {preds_path} is not a valid float: {actual}")

        assert abs(expected - actual_val) < 1e-3, f"Mismatch at test sample {idx+1}: expected {expected:.4f}, got {actual_val:.4f}. Check your normalizer or loop bounds."