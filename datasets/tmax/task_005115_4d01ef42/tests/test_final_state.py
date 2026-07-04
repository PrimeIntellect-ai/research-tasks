# test_final_state.py

import os
import re
import math
import pytest

def test_join_data_script_exists():
    path = "/home/user/join_data.sh"
    assert os.path.isfile(path), f"File {path} is missing."

def test_infer_c_and_executable_exist():
    c_path = "/home/user/infer.c"
    exe_path = "/home/user/infer_model"
    assert os.path.isfile(c_path), f"File {c_path} is missing."
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_joined_sensor_data():
    path = "/home/user/joined_sensor_data.csv"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_header = "id,temperature,vibration"
    assert lines[0] == expected_header, f"Header of {path} is incorrect."

    expected_data = [
        "1,22.5,1.1",
        "2,45.1,4.8",
        "3,18.0,0.9",
        "4,60.2,5.5",
        "5,30.5,2.0"
    ]

    assert lines[1:] == expected_data, f"Data in {path} does not match expected joined data."

def test_predictions_csv():
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines[0] == "id,probability,class", f"Header of {path} is incorrect."

    # Compute expected predictions
    inputs = [
        (1, 22.5, 1.1),
        (2, 45.1, 4.8),
        (3, 18.0, 0.9),
        (4, 60.2, 5.5),
        (5, 30.5, 2.0)
    ]

    expected_data = []
    for i, t, v in inputs:
        z = 0.5 * t + 1.2 * v - 15.0
        p = 1.0 / (1.0 + math.exp(-z))
        cls = 1 if p > 0.5 else 0
        expected_data.append(f"{i},{p:.4f},{cls}")

    assert lines[1:] == expected_data, f"Predictions in {path} do not match mathematically expected values."

def test_benchmark_txt():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    pattern = r"^Inference Time:\s*\d+\s*us$"
    assert re.match(pattern, content), f"Content of {path} ('{content}') does not match expected format 'Inference Time: <time_in_microseconds> us'."