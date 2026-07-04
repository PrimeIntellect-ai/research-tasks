# test_final_state.py

import os
import math

def test_corr_c_exists():
    path = "/home/user/corr.c"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a regular file."
    with open(path, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, f"{path} is empty."

def test_corr_executable_exists():
    path = "/home/user/corr"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a regular file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_result_txt():
    dataset_path = "/home/user/dataset.tsv"
    result_path = "/home/user/result.txt"

    assert os.path.exists(dataset_path), f"Dataset {dataset_path} is missing."
    assert os.path.exists(result_path), f"Result file {result_path} does not exist."

    # Calculate the expected correlation using standard library
    x = []
    y = []
    with open(dataset_path, "r") as f:
        for line in f:
            parts = line.strip("\n").split("\t")
            if len(parts) >= 4:
                x.append(float(parts[1]))
                y.append(float(parts[3]))

    n = len(x)
    assert n > 0, "Dataset is empty."

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)

    corr = cov / math.sqrt(var_x * var_y)
    expected_result = f"{corr:.4f}"

    with open(result_path, "r") as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, f"Expected result {expected_result}, but got {actual_result} in {result_path}."