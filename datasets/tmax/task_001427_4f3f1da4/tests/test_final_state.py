# test_final_state.py
import os
import csv
import math
import pytest

def test_process_go_exists():
    assert os.path.isfile("/home/user/process.go"), "/home/user/process.go is missing"

def test_process_executable_exists():
    assert os.path.isfile("/home/user/process"), "/home/user/process executable is missing"
    assert os.access("/home/user/process", os.X_OK), "/home/user/process is not executable"

def test_results_csv_correct():
    sensors_file = "/home/user/sensors.csv"
    results_file = "/home/user/results.csv"

    assert os.path.isfile(sensors_file), f"{sensors_file} is missing"
    assert os.path.isfile(results_file), f"{results_file} is missing"

    sensors = []
    with open(sensors_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensors.append({
                "sensor_id": row["sensor_id"],
                "val_x": float(row["val_x"]),
                "val_y": float(row["val_y"]),
                "prior_fail": float(row["prior_fail"]),
                "p_high_given_fail": float(row["p_high_given_fail"]),
                "p_high_given_ok": float(row["p_high_given_ok"]),
                "is_high": int(row["is_high"])
            })

    expected_results = []
    for i, s in enumerate(sensors):
        # Calculate posterior
        prior_fail = s["prior_fail"]
        prior_ok = 1.0 - prior_fail

        if s["is_high"] == 1:
            likelihood_fail = s["p_high_given_fail"]
            likelihood_ok = s["p_high_given_ok"]
        else:
            likelihood_fail = 1.0 - s["p_high_given_fail"]
            likelihood_ok = 1.0 - s["p_high_given_ok"]

        marginal = (likelihood_fail * prior_fail) + (likelihood_ok * prior_ok)
        posterior = (likelihood_fail * prior_fail) / marginal
        posterior_str = f"{posterior:.4f}"

        # Find nearest neighbor
        nearest_id = None
        min_dist = float('inf')
        for j, other in enumerate(sensors):
            if i == j:
                continue
            dist = math.hypot(s["val_x"] - other["val_x"], s["val_y"] - other["val_y"])
            if dist < min_dist:
                min_dist = dist
                nearest_id = other["sensor_id"]

        expected_results.append({
            "sensor_id": s["sensor_id"],
            "posterior_fail_prob": posterior_str,
            "nearest_sensor_id": nearest_id
        })

    actual_results = []
    with open(results_file, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["sensor_id", "posterior_fail_prob", "nearest_sensor_id"], "Results CSV header is incorrect"
        for row in reader:
            actual_results.append(row)

    assert len(actual_results) == len(expected_results), "Number of rows in results.csv does not match sensors.csv"

    for expected, actual in zip(expected_results, actual_results):
        assert actual["sensor_id"] == expected["sensor_id"], f"Expected sensor_id {expected['sensor_id']}, got {actual['sensor_id']}"
        assert actual["posterior_fail_prob"] == expected["posterior_fail_prob"], f"Incorrect posterior probability for {expected['sensor_id']}"
        assert actual["nearest_sensor_id"] == expected["nearest_sensor_id"], f"Incorrect nearest neighbor for {expected['sensor_id']}"