# test_final_state.py

import os
import random

def test_executable_exists():
    exe_path = "/home/user/bin/score_ext"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_dataset_csv_contents():
    dataset_path = "/home/user/dataset.csv"
    assert os.path.isfile(dataset_path), f"Dataset file {dataset_path} does not exist."

    target_path = "/home/user/target.txt"
    assert os.path.isfile(target_path), f"Target file {target_path} is missing."
    with open(target_path, "r") as f:
        target = f.read().strip()

    # Generate expected data
    random.seed(123)
    expected_lines = []
    for _ in range(100):
        primer = "".join(random.choices("ACGT", k=12))
        max_score = 0
        for i in range(len(target) - 12 + 1):
            score = sum(1 for j in range(12) if primer[j] == target[i+j])
            if score > max_score:
                max_score = score
        expected_lines.append(f"{primer},{max_score}")

    with open(dataset_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 100, f"Expected 100 lines in {dataset_path}, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."