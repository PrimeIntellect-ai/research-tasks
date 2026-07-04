# test_final_state.py

import os
import subprocess
import pytest
from collections import defaultdict

@pytest.fixture(scope="session", autouse=True)
def run_etl_script():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script to ensure the pipeline executes from start to finish
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}\nOutput:\n{result.stdout}"

def test_features_csv_correctness():
    features_path = "/home/user/features.csv"
    assert os.path.isfile(features_path), f"Missing required file: {features_path}"

    # Compute expected aggregations
    logs = defaultdict(lambda: {"count": 0, "payload": 0, "resp": 0})
    with open("/home/user/raw_logs.txt", "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(" | ")
            ip = parts[1]
            resp = int(parts[2])
            payload = int(parts[3])
            logs[ip]["count"] += 1
            logs[ip]["payload"] += payload
            logs[ip]["resp"] += resp

    labels = {}
    with open("/home/user/labels.csv", "r") as f:
        for line in f:
            if not line.strip():
                continue
            ip, label = line.strip().split(",")
            labels[ip] = int(label)

    expected_rows = []
    # Ensure sorted by IP address ascending
    for ip in sorted(labels.keys()):
        if ip in logs:
            count = logs[ip]["count"]
            payload = logs[ip]["payload"]
            avg_resp = logs[ip]["resp"] // count
            expected_rows.append(f"{ip},{count},{payload},{avg_resp},{labels[ip]}")

    with open(features_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_rows), f"Expected {len(expected_rows)} rows in features.csv, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"

def test_train_script_exists():
    train_path = "/home/user/train.py"
    assert os.path.isfile(train_path), f"Python script {train_path} was not created."

def test_accuracy_file():
    acc_path = "/home/user/accuracy.txt"
    assert os.path.isfile(acc_path), f"Missing required file: {acc_path}"

    with open(acc_path, "r") as f:
        content = f.read().strip()

    try:
        acc = float(content)
    except ValueError:
        pytest.fail(f"Accuracy file does not contain a valid float: {content}")

    assert 0.0 <= acc <= 1.0, f"Accuracy {acc} is out of valid range [0, 1]"
    assert acc > 0.8, f"Accuracy {acc} is too low. Expected > 0.8 given the dataset separation."