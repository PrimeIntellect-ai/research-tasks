# test_final_state.py

import os
import csv
import pytest

def test_predictions_mse():
    predictions_path = "/home/user/predictions.csv"
    assert os.path.isfile(predictions_path), f"Predictions file missing at {predictions_path}"

    # Hidden ground truth for the evaluation dataset
    truth = {
        "2001": 140.0,
        "2002": 146.0,
        "2003": 150.0
    }

    sum_sq_err = 0.0
    count = 0

    with open(predictions_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "Predictions file is empty or missing a header"

        for row in reader:
            if not row or len(row) < 2:
                continue

            ts = row[0].strip()
            if ts in truth:
                try:
                    pred = float(row[1].strip())
                    diff = pred - truth[ts]
                    sum_sq_err += diff * diff
                    count += 1
                except ValueError:
                    pytest.fail(f"Invalid predicted value for timestamp {ts}: '{row[1]}'")

    assert count > 0, "No valid predictions found for the evaluation timestamps."

    mse = sum_sq_err / count
    threshold = 0.5

    assert mse <= threshold, f"MSE {mse:.4f} exceeds the threshold of {threshold}."

def test_auxiliary_files_exist():
    clean_data_path = "/home/user/clean_data.csv"
    model_stats_path = "/home/user/model_stats.txt"

    assert os.path.isfile(clean_data_path), f"Cleaned dataset missing at {clean_data_path}"
    assert os.path.isfile(model_stats_path), f"Model stats file missing at {model_stats_path}"