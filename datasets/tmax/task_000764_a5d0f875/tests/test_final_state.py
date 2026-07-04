# test_final_state.py

import os
import re
import pytest
import subprocess

def test_smoother_compiled():
    smoother_path = "/home/user/bin/smoother"
    assert os.path.isfile(smoother_path), f"Executable {smoother_path} is missing."
    assert os.access(smoother_path, os.X_OK), f"File {smoother_path} is not executable."

def test_processed_data_exists():
    processed_file = "/home/user/data/processed/spectrum_smoothed.csv"
    assert os.path.isfile(processed_file), f"Processed data file {processed_file} is missing."

    # Check if it has content
    with open(processed_file, "r") as f:
        lines = f.readlines()
    assert len(lines) > 1, f"Processed data file {processed_file} does not contain enough data."
    assert "wavelength,intensity" in lines[0], "Header missing in smoothed CSV."

def test_optimize_script_exists():
    script_path = "/home/user/optimize.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_best_fit_output():
    best_fit_file = "/home/user/best_fit.txt"
    assert os.path.isfile(best_fit_file), f"Output file {best_fit_file} is missing."

    with open(best_fit_file, "r") as f:
        content = f.read().strip()

    # Expected format: mu1=[BEST_MU1],mu2=[BEST_MU2],mse=[MIN_MSE]
    match = re.match(r"^mu1=(\d+),mu2=(\d+),mse=([0-9.]+)$", content)
    assert match is not None, f"Content of {best_fit_file} does not match the required format: mu1=[BEST_MU1],mu2=[BEST_MU2],mse=[MIN_MSE]. Found: {content}"

    mu1 = int(match.group(1))
    mu2 = int(match.group(2))
    mse = float(match.group(3))

    assert mu1 == 126, f"Expected mu1 to be 126, but got {mu1}."
    assert mu2 == 344, f"Expected mu2 to be 344, but got {mu2}."
    assert 0.40 < mse < 0.42, f"Expected mse to be around 0.4079, but got {mse}."