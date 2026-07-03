# test_final_state.py
import os
import subprocess
import math

def test_prepare_data_script_runs():
    script_path = "/home/user/scripts/prepare_data.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"prepare_data.sh failed to run. Stderr: {result.stderr}"

    assert os.path.isfile("/home/user/data/train_scaled.csv"), "train_scaled.csv was not created"
    assert os.path.isfile("/home/user/data/test_scaled.csv"), "test_scaled.csv was not created"

def test_scaled_data_correctness():
    raw_csv = "/home/user/data/raw.csv"
    train_scaled_csv = "/home/user/data/train_scaled.csv"
    test_scaled_csv = "/home/user/data/test_scaled.csv"

    with open(raw_csv, "r") as f:
        raw_data = [line.strip().split(",") for line in f if line.strip()]

    assert len(raw_data) == 100, "raw.csv should have exactly 100 lines"

    train_raw = raw_data[:80]
    test_raw = raw_data[80:]

    # Calculate population mean and std on train data only
    sum1 = sum(float(row[0]) for row in train_raw)
    sum2 = sum(float(row[1]) for row in train_raw)
    mean1 = sum1 / 80.0
    mean2 = sum2 / 80.0

    sumsq1 = sum((float(row[0]) - mean1)**2 for row in train_raw)
    sumsq2 = sum((float(row[1]) - mean2)**2 for row in train_raw)
    std1 = math.sqrt(sumsq1 / 80.0)
    std2 = math.sqrt(sumsq2 / 80.0)

    def check_scaled_file(filepath, raw_subset):
        with open(filepath, "r") as f:
            scaled_data = [line.strip().split(",") for line in f if line.strip()]

        assert len(scaled_data) == len(raw_subset), f"{filepath} has incorrect number of rows"

        for i, (scaled_row, raw_row) in enumerate(zip(scaled_data, raw_subset)):
            expected_x1 = (float(raw_row[0]) - mean1) / std1
            expected_x2 = (float(raw_row[1]) - mean2) / std2
            expected_y = raw_row[2]

            assert abs(float(scaled_row[0]) - expected_x1) < 1e-4, f"Row {i+1} in {filepath} X1 is incorrect. Expected {expected_x1}, got {scaled_row[0]}"
            assert abs(float(scaled_row[1]) - expected_x2) < 1e-4, f"Row {i+1} in {filepath} X2 is incorrect. Expected {expected_x2}, got {scaled_row[1]}"
            assert scaled_row[2] == expected_y, f"Row {i+1} in {filepath} y is incorrect. Expected {expected_y}, got {scaled_row[2]}"

    check_scaled_file(train_scaled_csv, train_raw)
    check_scaled_file(test_scaled_csv, test_raw)

def test_bootstrap_script_runs():
    script_path = "/home/user/scripts/bootstrap.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"bootstrap.sh failed to run. Stderr: {result.stderr}"

    for i in range(1, 6):
        boot_file = f"/home/user/data/boot_{i}.csv"
        assert os.path.isfile(boot_file), f"{boot_file} was not created"

def test_bootstrap_files_correctness():
    train_scaled_csv = "/home/user/data/train_scaled.csv"
    with open(train_scaled_csv, "r") as f:
        train_lines = set(line.strip() for line in f if line.strip())

    for i in range(1, 6):
        boot_file = f"/home/user/data/boot_{i}.csv"
        with open(boot_file, "r") as f:
            boot_data = [line.strip() for line in f if line.strip()]

        assert len(boot_data) == 80, f"{boot_file} should have exactly 80 rows, got {len(boot_data)}"

        for j, line in enumerate(boot_data):
            assert line in train_lines, f"Line {j+1} in {boot_file} is not from train_scaled.csv: {line}"