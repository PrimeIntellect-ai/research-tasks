# test_final_state.py

import os
import csv
import pytest

def test_best_threshold_file():
    path = "/home/user/best_threshold.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "30", f"Expected best threshold to be '30', but got '{content}'"

def test_tuning_results_file():
    path = "/home/user/tuning_results.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    expected_accuracies = {
        "10": 0.8,
        "20": 0.9,
        "30": 1.0,
        "40": 0.9,
        "50": 0.8
    }

    with open(path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "tuning_results.csv is empty"
    header = rows[0]
    assert header == ["threshold", "accuracy", "time_ms"], f"Incorrect header in tuning_results.csv: {header}"

    assert len(rows) == 6, f"Expected 5 data rows in tuning_results.csv, got {len(rows)-1}"

    found_thresholds = set()
    for row in rows[1:]:
        assert len(row) == 3, f"Row does not have 3 columns: {row}"
        threshold, accuracy, time_ms = row

        assert threshold in expected_accuracies, f"Unexpected threshold: {threshold}"
        found_thresholds.add(threshold)

        try:
            acc_val = float(accuracy)
        except ValueError:
            pytest.fail(f"Accuracy is not a float: {accuracy}")

        expected_acc = expected_accuracies[threshold]
        assert abs(acc_val - expected_acc) < 1e-5, f"Expected accuracy {expected_acc} for threshold {threshold}, got {acc_val}"

        try:
            time_val = float(time_ms)
            assert time_val > 0, f"Expected positive time_ms, got {time_val}"
        except ValueError:
            pytest.fail(f"time_ms is not a number: {time_ms}")

    assert found_thresholds == set(expected_accuracies.keys()), "Missing thresholds in tuning_results.csv"

def test_run_pipeline_exists():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Missing file: {path}"
    assert os.access(path, os.X_OK) or os.stat(path).st_mode & 0o111, f"File is not executable: {path}"