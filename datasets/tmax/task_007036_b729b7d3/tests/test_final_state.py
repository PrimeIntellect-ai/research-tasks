# test_final_state.py

import os
import csv
import pytest

RAW_METRICS_PATH = "/home/user/raw_metrics.csv"
CLEAN_FEATURES_PATH = "/home/user/clean_features.csv"
PREDICTIONS_PATH = "/home/user/predictions.txt"
REPORT_PATH = "/home/user/report.txt"

def get_expected_clean_features():
    expected_rows = []
    if not os.path.exists(RAW_METRICS_PATH):
        return []

    with open(RAW_METRICS_PATH, "r") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
        except StopIteration:
            return []

        for row in reader:
            if len(row) != 6:
                continue
            timestamp, cpu, mem, net_in, net_out, err = row

            # Filter empty values
            if not all(row):
                continue

            # Filter error flag
            if err == "1":
                continue

            # Convert net_in and net_out
            try:
                net_in_mb = float(net_in) / 1024.0
                net_out_mb = float(net_out) / 1024.0
            except ValueError:
                continue

            expected_rows.append(f"{cpu},{mem},{net_in_mb:.2f},{net_out_mb:.2f}")

    return expected_rows

def get_expected_predictions(clean_rows):
    predictions = []
    for row in clean_rows:
        cols = row.split(",")
        cpu = float(cols[0])
        mem = float(cols[1])
        net_in = float(cols[2])
        net_out = float(cols[3])

        score = (0.6 * cpu) + (0.3 * mem) + (0.05 * net_in) + (0.05 * net_out) - 65.0
        predictions.append(1 if score > 0 else 0)
    return predictions

def test_clean_features_csv():
    assert os.path.isfile(CLEAN_FEATURES_PATH), f"File {CLEAN_FEATURES_PATH} does not exist."

    expected_rows = get_expected_clean_features()

    with open(CLEAN_FEATURES_PATH, "r") as f:
        actual_content = f.read().strip().splitlines()

    assert actual_content == expected_rows, f"Content of {CLEAN_FEATURES_PATH} does not match expected cleaned data."

def test_predictions_txt():
    assert os.path.isfile(PREDICTIONS_PATH), f"File {PREDICTIONS_PATH} does not exist."

    expected_clean_rows = get_expected_clean_features()
    expected_preds = get_expected_predictions(expected_clean_rows)
    expected_preds_str = [str(p) for p in expected_preds]

    with open(PREDICTIONS_PATH, "r") as f:
        actual_preds = f.read().strip().splitlines()

    assert actual_preds == expected_preds_str, f"Content of {PREDICTIONS_PATH} does not match expected predictions."

def test_report_txt():
    assert os.path.isfile(REPORT_PATH), f"File {REPORT_PATH} does not exist."

    expected_clean_rows = get_expected_clean_features()
    expected_preds = get_expected_predictions(expected_clean_rows)

    expected_report = [
        str(len(expected_clean_rows)),
        str(sum(expected_preds)),
        "Pipeline Complete"
    ]

    with open(REPORT_PATH, "r") as f:
        actual_report = f.read().strip().splitlines()

    assert actual_report == expected_report, f"Content of {REPORT_PATH} does not match expected report."