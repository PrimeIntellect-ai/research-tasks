# test_final_state.py

import os
import csv
import math
import pytest

def test_evaluate_go_exists():
    assert os.path.isfile("/home/user/evaluate.go"), "/home/user/evaluate.go is missing. You must save your Go program at this path."

def test_validation_txt_correctness():
    validation_file = "/home/user/validation.txt"
    input_file = "/home/user/input.csv"
    weights_file = "/home/user/weights.csv"

    assert os.path.isfile(validation_file), f"{validation_file} is missing. Did you run your Go program?"
    assert os.path.isfile(input_file), f"{input_file} is missing."
    assert os.path.isfile(weights_file), f"{weights_file} is missing."

    # Read weights
    with open(weights_file, "r") as f:
        weights_str = f.read().strip()
    weights = [float(w) for w in weights_str.split(",")]
    assert len(weights) == 3, "Weights file should contain exactly 3 weights."

    # Read input and compute expected results
    sq_errors = []
    anomalies = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = int(row['id'])
            v1, v2, v3 = float(row['v1']), float(row['v2']), float(row['v3'])
            target = float(row['target'])

            y_pred = v1 * weights[0] + v2 * weights[1] + v3 * weights[2]
            error = y_pred - target
            sq_errors.append(error ** 2)

            if abs(error) > 2.0:
                anomalies.append(row_id)

    expected_mse = sum(sq_errors) / len(sq_errors)
    expected_mse_str = f"MSE: {expected_mse:.4f}"

    expected_lines = [expected_mse_str, "Anomalies:"] + [str(a) for a in anomalies]
    expected_content = "\n".join(expected_lines)

    with open(validation_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {validation_file} is incorrect.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )