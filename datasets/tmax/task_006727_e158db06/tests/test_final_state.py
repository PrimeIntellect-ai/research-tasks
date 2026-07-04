# test_final_state.py
import os
import pytest

def test_predictions_csv_correct():
    preds_path = "/home/user/predictions.csv"
    assert os.path.isfile(preds_path), f"File missing: {preds_path}"

    with open(preds_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in predictions.csv, found {len(lines)}"

    # Check numeric values to avoid minor formatting differences (like -1 vs -1.0)
    expected_values = [
        (1, 7.6, 8.6),
        (3, -1.0, -1.5),
        (5, 13.8, 13.8)
    ]

    for i, line in enumerate(lines):
        parts = line.split(',')
        assert len(parts) == 3, f"Line {i+1} does not have 3 comma-separated values: {line}"
        try:
            vals = (int(parts[0]), float(parts[1]), float(parts[2]))
        except ValueError:
            pytest.fail(f"Line {i+1} contains non-numeric values: {line}")

        assert vals[0] == expected_values[i][0], f"ID mismatch on line {i+1}: expected {expected_values[i][0]}, got {vals[0]}"
        assert abs(vals[1] - expected_values[i][1]) < 1e-6, f"Prediction mismatch on line {i+1}: expected {expected_values[i][1]}, got {vals[1]}"
        assert abs(vals[2] - expected_values[i][2]) < 1e-6, f"Target mismatch on line {i+1}: expected {expected_values[i][2]}, got {vals[2]}"

def test_metrics_log_correct():
    metrics_path = "/home/user/metrics.log"
    assert os.path.isfile(metrics_path), f"File missing: {metrics_path}"

    with open(metrics_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{metrics_path} is empty"

    last_line = lines[-1]

    # The requirement says exactly "MAE=0.5" but let's be robust to minor float formatting like "MAE=0.50"
    assert last_line.startswith("MAE="), f"Last line of {metrics_path} does not start with MAE=: {last_line}"

    try:
        mae_val = float(last_line.split("=")[1])
    except ValueError:
        pytest.fail(f"Could not parse MAE value from last line: {last_line}")

    assert abs(mae_val - 0.5) < 1e-6, f"MAE value mismatch: expected 0.5, got {mae_val}"