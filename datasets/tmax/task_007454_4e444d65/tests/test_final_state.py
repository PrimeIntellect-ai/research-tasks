# test_final_state.py

import os
import re
import math
import pytest

WORKSPACE_DIR = "/home/user/ml_pipeline"

def load_csv(filepath):
    with open(filepath, 'r') as f:
        return [line.strip().split(',') for line in f if line.strip()]

def test_files_exist():
    expected_files = [
        "train_scaled.csv",
        "test_scaled.csv",
        "model.pkl",
        "benchmark.sh",
        "avg_time.txt"
    ]
    for filename in expected_files:
        path = os.path.join(WORKSPACE_DIR, filename)
        assert os.path.isfile(path), f"Expected file {path} is missing."

def test_benchmark_script_executable():
    path = os.path.join(WORKSPACE_DIR, "benchmark.sh")
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_avg_time_format():
    path = os.path.join(WORKSPACE_DIR, "avg_time.txt")
    with open(path, 'r') as f:
        content = f.read().strip()

    match = re.match(r"^Average Inference Time: [0-9.]+ ms$", content)
    assert match is not None, f"avg_time.txt content '{content}' does not match expected format 'Average Inference Time: <value> ms'."

def test_data_leakage_fixed():
    # Recompute the expected data
    users_path = os.path.join(WORKSPACE_DIR, "users.csv")
    transactions_path = os.path.join(WORKSPACE_DIR, "transactions.csv")

    assert os.path.isfile(users_path), "users.csv is missing. Did you run generate_data.py?"
    assert os.path.isfile(transactions_path), "transactions.csv is missing. Did you run generate_data.py?"

    users = load_csv(users_path)
    transactions = load_csv(transactions_path)

    # Sort by user_id
    users.sort(key=lambda x: x[0])
    transactions.sort(key=lambda x: x[0])

    # Join on user_id
    joined = []
    t_idx = 0
    for u in users:
        while t_idx < len(transactions) and transactions[t_idx][0] < u[0]:
            t_idx += 1
        if t_idx < len(transactions) and transactions[t_idx][0] == u[0]:
            # user_id, age, amount, fraud_label
            joined.append([u[0], u[1], transactions[t_idx][1], transactions[t_idx][2]])

    assert len(joined) == 1000, f"Expected 1000 joined rows, got {len(joined)}."

    train_raw = joined[:800]
    test_raw = joined[800:]

    # Compute min/max on train_raw
    train_amounts = [float(row[2]) for row in train_raw]
    min_amt = min(train_amounts)
    max_amt = max(train_amounts)

    # Scale
    def scale_row(row):
        scaled = (float(row[2]) - min_amt) / (max_amt - min_amt)
        return f"{row[0]},{row[1]},{scaled:.4f},{row[3]}"

    expected_train = [scale_row(row) for row in train_raw]
    expected_test = [scale_row(row) for row in test_raw]

    # Load actual
    actual_train = [",".join(row) for row in load_csv(os.path.join(WORKSPACE_DIR, "train_scaled.csv"))]
    actual_test = [",".join(row) for row in load_csv(os.path.join(WORKSPACE_DIR, "test_scaled.csv"))]

    assert len(actual_train) == 800, f"train_scaled.csv should have 800 rows, got {len(actual_train)}"
    assert len(actual_test) == 200, f"test_scaled.csv should have 200 rows, got {len(actual_test)}"

    for i, (act, exp) in enumerate(zip(actual_train, expected_train)):
        assert act == exp, f"Mismatch in train_scaled.csv at row {i+1}. Expected '{exp}', got '{act}'."

    for i, (act, exp) in enumerate(zip(actual_test, expected_test)):
        assert act == exp, f"Mismatch in test_scaled.csv at row {i+1}. Expected '{exp}', got '{act}'."