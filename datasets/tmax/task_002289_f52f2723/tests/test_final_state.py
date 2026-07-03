# test_final_state.py

import os
import csv
import re

def compute_expected_mse(csv_path, iterations=1000, sample_size=50, seed=42):
    dataset = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            if not row:
                continue
            dataset.append((float(row[0]), float(row[1])))

    N = len(dataset)
    state = seed
    total_mse = 0.0

    for _ in range(iterations):
        sample_mse = 0.0
        for _ in range(sample_size):
            state = (1103515245 * state + 12345) % 2147483648
            idx = state % N
            x, true_y = dataset[idx]
            pred_y = 2.5 + 1.2 * x - 0.3 * (x**2)
            sample_mse += (pred_y - true_y)**2
        total_mse += sample_mse / sample_size

    avg_mse = total_mse / iterations
    return f"{avg_mse:.4f}"

def test_evaluator_cpp_exists():
    assert os.path.exists("/home/user/evaluator.cpp"), "/home/user/evaluator.cpp does not exist."

def test_evaluator_binary_exists():
    assert os.path.exists("/home/user/evaluator"), "/home/user/evaluator does not exist."
    assert os.access("/home/user/evaluator", os.X_OK), "/home/user/evaluator is not executable."

def test_results_file_exists():
    assert os.path.exists("/home/user/results.txt"), "/home/user/results.txt does not exist."

def test_results_contents():
    csv_path = "/home/user/dataset.csv"
    assert os.path.exists(csv_path), f"{csv_path} is missing."

    expected_mse = compute_expected_mse(csv_path)

    with open("/home/user/results.txt", "r") as f:
        content = f.read()

    mse_match = re.search(r"Avg_MSE:\s*([\d\.]+)", content)
    assert mse_match is not None, "Avg_MSE not found in /home/user/results.txt"
    actual_mse = mse_match.group(1)

    assert actual_mse == expected_mse, f"Expected Avg_MSE to be {expected_mse}, got {actual_mse}"

    time_match = re.search(r"Avg_Time_us:\s*([\d\.]+)", content)
    assert time_match is not None, "Avg_Time_us not found in /home/user/results.txt"
    actual_time = float(time_match.group(1))

    assert actual_time >= 0, f"Expected Avg_Time_us to be >= 0, got {actual_time}"