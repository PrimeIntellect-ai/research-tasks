# test_final_state.py

import os
import pytest

def compute_expected_accuracy(data_path):
    with open(data_path, "r") as f:
        lines = f.read().strip().split("\n")

    data = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(",")
        data.append({
            "x": float(parts[0]),
            "y": float(parts[1]),
            "label": int(parts[2])
        })

    train_size = 80
    test_size = len(data) - train_size

    # Calculate mean on train data only
    mean_x = sum(d["x"] for d in data[:train_size]) / train_size
    mean_y = sum(d["y"] for d in data[:train_size]) / train_size

    # Projection
    for d in data:
        centered_x = d["x"] - mean_x
        centered_y = d["y"] - mean_y
        d["projected"] = (centered_x + centered_y) / 2.0

    # Training
    mean_class0 = 0.0
    mean_class1 = 0.0
    count0 = 0
    count1 = 0
    for d in data[:train_size]:
        if d["label"] == 0:
            mean_class0 += d["projected"]
            count0 += 1
        else:
            mean_class1 += d["projected"]
            count1 += 1

    if count0 > 0: mean_class0 /= count0
    if count1 > 0: mean_class1 /= count1

    # Testing
    correct = 0
    for d in data[train_size:]:
        dist0 = abs(d["projected"] - mean_class0)
        dist1 = abs(d["projected"] - mean_class1)
        pred = 0 if dist0 < dist1 else 1
        if pred == d["label"]:
            correct += 1

    return correct / test_size

def test_fixed_metrics_file():
    metrics_path = "/home/user/fixed_metrics.txt"
    data_path = "/home/user/mlops_exp/data.csv"

    assert os.path.isfile(metrics_path), f"File {metrics_path} does not exist."
    assert os.path.isfile(data_path), f"File {data_path} does not exist."

    expected_acc = compute_expected_accuracy(data_path)

    with open(metrics_path, "r") as f:
        content = f.read().strip()

    try:
        actual_acc = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {metrics_path}.")

    assert abs(actual_acc - expected_acc) < 1e-6, f"Expected accuracy {expected_acc}, but got {actual_acc} in {metrics_path}."

def test_cpp_code_fixed():
    cpp_path = "/home/user/mlops_exp/pca_bayes.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    # The mean calculation should now use train_size
    # We check if the division uses train_size
    assert "mean_x /= train_size;" in content or "mean_x /= (double)train_size;" in content or "mean_x /= (float)train_size;" in content or "mean_x = mean_x / train_size;" in content.replace(" ", ""), "The C++ code does not seem to divide by train_size for mean_x."
    assert "mean_y /= train_size;" in content or "mean_y /= (double)train_size;" in content or "mean_y /= (float)train_size;" in content or "mean_y = mean_y / train_size;" in content.replace(" ", ""), "The C++ code does not seem to divide by train_size for mean_y."

    # Ensure it no longer divides by total_size
    assert "mean_x /= total_size;" not in content, "The C++ code still divides by total_size for mean_x."
    assert "mean_y /= total_size;" not in content, "The C++ code still divides by total_size for mean_y."

def test_cpp_binary_exists():
    bin_path = "/home/user/mlops_exp/pca_bayes"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."