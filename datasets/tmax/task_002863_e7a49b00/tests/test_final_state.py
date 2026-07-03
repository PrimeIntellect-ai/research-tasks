# test_final_state.py

import os
import math

def test_predictions_exist():
    """Check if the predictions file exists."""
    assert os.path.isfile('/home/user/predictions.txt'), "The file /home/user/predictions.txt is missing."

def test_predictions_correctness():
    """Verify the predictions are correctly calculated without data leakage."""
    csv_path = '/home/user/data/raw.csv'
    pred_path = '/home/user/predictions.txt'

    assert os.path.isfile(csv_path), f"The file {csv_path} is missing."
    assert os.path.isfile(pred_path), f"The file {pred_path} is missing."

    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 101, "Expected exactly 101 lines in raw.csv (header + 100 rows)."

    # Parse data
    data = []
    for line in lines[1:]:
        parts = line.split(',')
        assert len(parts) == 3, "Invalid CSV format."
        data.append([float(parts[0]), float(parts[1]), float(parts[2])])

    # Split train and test
    train_data = data[:80]
    test_data = data[80:]

    assert len(test_data) == 20, "Expected exactly 20 test rows."

    # Calculate min/max from train data ONLY
    min_age = min(row[0] for row in train_data)
    max_age = max(row[0] for row in train_data)

    min_income = min(row[1] for row in train_data)
    max_income = max(row[1] for row in train_data)

    min_score = min(row[2] for row in train_data)
    max_score = max(row[2] for row in train_data)

    # Calculate expected predictions
    expected_preds = []
    for row in test_data:
        scaled_age = (row[0] - min_age) / (max_age - min_age)
        scaled_income = (row[1] - min_income) / (max_income - min_income)
        scaled_score = (row[2] - min_score) / (max_score - min_score)

        pred = 5.0 + (2.5 * scaled_age) + (0.5 * scaled_income) + (-1.2 * scaled_score)
        expected_preds.append(pred)

    # Read actual predictions
    with open(pred_path, 'r') as f:
        actual_lines = f.read().strip().split('\n')

    assert len(actual_lines) == 20, f"Expected exactly 20 lines in predictions.txt, found {len(actual_lines)}."

    for i, (actual_str, expected) in enumerate(zip(actual_lines, expected_preds)):
        try:
            actual = float(actual_str)
        except ValueError:
            assert False, f"Prediction at line {i+1} is not a valid float: '{actual_str}'"

        diff = abs(actual - expected)
        assert diff < 1e-4, (
            f"Prediction mismatch at line {i+1} (test row {i+81}).\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}\n"
            f"Difference: {diff}\n"
            "Ensure min/max are calculated ONLY on the first 80 rows and applied correctly."
        )