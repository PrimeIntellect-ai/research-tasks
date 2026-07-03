# test_final_state.py

import os
import subprocess
import pytest

def test_baseline_load_csv():
    csv_path = "/home/user/baseline_load.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 100, f"Expected 100 lines in {csv_path}, found {len(lines)}."
    for i, line in enumerate(lines):
        try:
            val = int(line.strip())
        except ValueError:
            pytest.fail(f"Line {i+1} in {csv_path} is not an integer: '{line}'")

def test_baseline_params_txt():
    params_path = "/home/user/baseline_params.txt"
    assert os.path.isfile(params_path), f"File {params_path} is missing."

    with open(params_path, "r") as f:
        content = f.read().strip()

    parts = content.split()
    assert len(parts) == 2, f"Expected 2 values in {params_path}, found {len(parts)}."

    try:
        mu = float(parts[0])
        sigma = float(parts[1])
    except ValueError:
        pytest.fail(f"Values in {params_path} are not valid floats: '{content}'")

    # Check if mu and sigma are within a reasonable range of the ground truth
    # True mu = 150000, True sigma = 5000
    assert 145000 <= mu <= 155000, f"Estimated mu ({mu}) is too far from expected 150000."
    assert 2000 <= sigma <= 8000, f"Estimated sigma ({sigma}) is too far from expected 5000."

def test_classifier_executable():
    classifier_path = "/home/user/classifier"
    assert os.path.isfile(classifier_path), f"Classifier executable {classifier_path} is missing."
    assert os.access(classifier_path, os.X_OK), f"File {classifier_path} is not executable."

def test_classifier_clean_corpus():
    classifier_path = "/home/user/classifier"
    clean_dir = "/app/traces/clean/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    files = os.listdir(clean_dir)
    assert len(files) > 0, f"No files found in {clean_dir}."

    failed_files = []
    for file in files:
        filepath = os.path.join(clean_dir, file)
        result = subprocess.run([classifier_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(file)

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean modified/rejected (expected exit 0). Offending files: {', '.join(failed_files[:5])}"

def test_classifier_evil_corpus():
    classifier_path = "/home/user/classifier"
    evil_dir = "/app/traces/evil/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."
    files = os.listdir(evil_dir)
    assert len(files) > 0, f"No files found in {evil_dir}."

    failed_files = []
    for file in files:
        filepath = os.path.join(evil_dir, file)
        result = subprocess.run([classifier_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(file)

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil bypassed (expected exit 1). Offending files: {', '.join(failed_files[:5])}"