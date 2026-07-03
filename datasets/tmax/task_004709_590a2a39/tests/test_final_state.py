# test_final_state.py
import os
import csv
import re

EDGE_ML_DIR = "/home/user/edge_ml"
RAW_DATA_PATH = os.path.join(EDGE_ML_DIR, "raw_data.csv")
CLEAN_DATA_PATH = os.path.join(EDGE_ML_DIR, "clean_data.csv")
MODEL_WEIGHTS_PATH = os.path.join(EDGE_ML_DIR, "model_weights.txt")
PREDICTIONS_PATH = os.path.join(EDGE_ML_DIR, "predictions.csv")
COVARIANCE_PATH = os.path.join(EDGE_ML_DIR, "covariance.txt")

def is_float(value):
    try:
        float(value)
        # Handle NaN and Infinity which are floats but not valid numeric values for this context
        if value.lower() in ['nan', 'inf', '-inf', 'infinity', '-infinity']:
            return False
        return True
    except ValueError:
        return False

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_expected_clean_data():
    expected_rows = []
    if not os.path.exists(RAW_DATA_PATH):
        return expected_rows

    with open(RAW_DATA_PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 7:
                continue
            if not is_int(row[0]):
                continue
            if not all(is_float(val) for val in row[1:]):
                continue
            expected_rows.append(row)
    return expected_rows

def get_expected_predictions(clean_data):
    if not os.path.exists(MODEL_WEIGHTS_PATH):
        return []

    with open(MODEL_WEIGHTS_PATH, 'r') as f:
        weights = [float(line.strip()) for line in f if line.strip()]

    if len(weights) != 6:
        return []

    b = weights[0]
    w = weights[1:]

    predictions = []
    for row in clean_data:
        row_id = row[0]
        features = [float(x) for x in row[1:6]]
        pred = b + sum(f * weight for f, weight in zip(features, w))
        predictions.append((row_id, f"{pred:.4f}"))
    return predictions

def get_expected_covariance(clean_data, predictions):
    if not clean_data or not predictions:
        return None

    n = len(clean_data)
    y_true = [float(row[6]) for row in clean_data]
    y_pred = [float(pred[1]) for pred in predictions]

    mean_true = sum(y_true) / n
    mean_pred = sum(y_pred) / n

    cov = sum((y_pred[i] - mean_pred) * (y_true[i] - mean_true) for i in range(n)) / n
    return f"{cov:.4f}"


def test_clean_data_csv():
    assert os.path.exists(CLEAN_DATA_PATH), f"File {CLEAN_DATA_PATH} does not exist."

    expected_clean_data = get_expected_clean_data()

    with open(CLEAN_DATA_PATH, 'r') as f:
        reader = csv.reader(f)
        actual_clean_data = [row for row in reader if row]

    assert len(actual_clean_data) == len(expected_clean_data), f"Expected {len(expected_clean_data)} valid rows in clean_data.csv, found {len(actual_clean_data)}."

    for actual, expected in zip(actual_clean_data, expected_clean_data):
        assert actual == expected, f"Row mismatch in clean_data.csv. Expected {expected}, got {actual}."

def test_predictions_csv():
    assert os.path.exists(PREDICTIONS_PATH), f"File {PREDICTIONS_PATH} does not exist."

    expected_clean_data = get_expected_clean_data()
    expected_predictions = get_expected_predictions(expected_clean_data)

    with open(PREDICTIONS_PATH, 'r') as f:
        reader = csv.reader(f)
        actual_predictions = [tuple(row) for row in reader if row]

    assert len(actual_predictions) == len(expected_predictions), f"Expected {len(expected_predictions)} predictions, found {len(actual_predictions)}."

    for actual, expected in zip(actual_predictions, expected_predictions):
        assert actual[0] == expected[0], f"ID mismatch in predictions.csv. Expected {expected[0]}, got {actual[0]}."
        # Compare as floats to allow for minor formatting differences (e.g., .5000 vs .5) if they strictly match the value
        assert float(actual[1]) == float(expected[1]), f"Prediction mismatch for ID {expected[0]}. Expected {expected[1]}, got {actual[1]}."
        # Also check the exact formatting as per instructions
        assert actual[1] == expected[1], f"Prediction formatting mismatch for ID {expected[0]}. Expected exactly '{expected[1]}', got '{actual[1]}'."

def test_covariance_txt():
    assert os.path.exists(COVARIANCE_PATH), f"File {COVARIANCE_PATH} does not exist."

    expected_clean_data = get_expected_clean_data()
    expected_predictions = get_expected_predictions(expected_clean_data)
    expected_covariance = get_expected_covariance(expected_clean_data, expected_predictions)

    with open(COVARIANCE_PATH, 'r') as f:
        actual_covariance = f.read().strip()

    assert actual_covariance == expected_covariance, f"Covariance mismatch. Expected exactly '{expected_covariance}', got '{actual_covariance}'."