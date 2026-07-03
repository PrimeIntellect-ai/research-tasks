# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_rust_project_exists():
    cargo_toml = "/home/user/tracker/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Rust project not found: {cargo_toml} is missing."

def test_predictions_json():
    predictions_file = "/home/user/experiments/predictions.json"
    assert os.path.isfile(predictions_file), f"Output file missing: {predictions_file} was not created."

    # Read metadata
    metadata = {}
    with open("/home/user/experiments/metadata.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metadata[row["run_id"]] = row["status"]

    # Read logs and filter by SUCCESS
    success_logs = []
    with open("/home/user/experiments/logs.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if metadata.get(row["run_id"]) == "SUCCESS":
                success_logs.append({
                    "run_id": row["run_id"],
                    "x1": float(row["x1"]),
                    "x2": float(row["x2"]),
                    "x3": float(row["x3"]),
                    "y_pred": float(row["y_pred"])
                })

    # Reconstruct model
    b = 0.0
    w1 = 0.0
    w2 = 0.0
    w3 = 0.0

    # Find baseline
    for log in success_logs:
        if log["x1"] == 0.0 and log["x2"] == 0.0 and log["x3"] == 0.0:
            b = log["y_pred"]
            break

    # Find weights
    for log in success_logs:
        if log["x1"] != 0.0 and log["x2"] == 0.0 and log["x3"] == 0.0:
            w1 = (log["y_pred"] - b) / log["x1"]
        elif log["x1"] == 0.0 and log["x2"] != 0.0 and log["x3"] == 0.0:
            w2 = (log["y_pred"] - b) / log["x2"]
        elif log["x1"] == 0.0 and log["x2"] == 0.0 and log["x3"] != 0.0:
            w3 = (log["y_pred"] - b) / log["x3"]

    # Compute expected predictions
    expected_predictions = []
    with open("/home/user/experiments/test.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t_id = row["test_id"]
            x1 = float(row["x1"])
            x2 = float(row["x2"])
            x3 = float(row["x3"])

            x_comp = (x1 * x2) + x3
            y_pred = (w1 * x1) + (w2 * x2) + (w3 * x3) + b

            expected_predictions.append({
                "test_id": t_id,
                "x_comp": x_comp,
                "y_pred": y_pred
            })

    # Read generated predictions
    with open(predictions_file, "r") as f:
        try:
            actual_predictions = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {predictions_file} does not contain valid JSON.")

    assert isinstance(actual_predictions, list), "The JSON output must be a list of objects."
    assert len(actual_predictions) == len(expected_predictions), f"Expected {len(expected_predictions)} predictions, but found {len(actual_predictions)}."

    # Compare actual and expected
    expected_dict = {item["test_id"]: item for item in expected_predictions}
    actual_dict = {item.get("test_id"): item for item in actual_predictions}

    for t_id, exp in expected_dict.items():
        assert t_id in actual_dict, f"Missing prediction for test_id: {t_id}"
        act = actual_dict[t_id]

        assert "x_comp" in act, f"Missing 'x_comp' in prediction for {t_id}"
        assert "y_pred" in act, f"Missing 'y_pred' in prediction for {t_id}"

        assert math.isclose(act["x_comp"], exp["x_comp"], rel_tol=1e-5, abs_tol=1e-5), \
            f"Incorrect x_comp for {t_id}: expected {exp['x_comp']}, got {act['x_comp']}"
        assert math.isclose(act["y_pred"], exp["y_pred"], rel_tol=1e-5, abs_tol=1e-5), \
            f"Incorrect y_pred for {t_id}: expected {exp['y_pred']}, got {act['y_pred']}"