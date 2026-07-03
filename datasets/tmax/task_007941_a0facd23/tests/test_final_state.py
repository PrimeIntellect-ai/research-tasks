# test_final_state.py

import os
import subprocess
import pytest

def test_venv_exists():
    venv_python = "/home/user/bio_env/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment python not found at {venv_python}"

def test_numpy_installed():
    venv_python = "/home/user/bio_env/bin/python"
    try:
        result = subprocess.run(
            [venv_python, "-c", "import numpy"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"numpy is not installed in the virtual environment. Error: {e.stderr}")

def test_smooth_executable_exists():
    smooth_bin = "/home/user/bin/smooth"
    assert os.path.isfile(smooth_bin), f"Compiled executable not found at {smooth_bin}"
    assert os.access(smooth_bin, os.X_OK), f"File at {smooth_bin} is not executable"

def test_smoothed_data_exists():
    smoothed_path = "/home/user/smoothed.txt"
    assert os.path.isfile(smoothed_path), f"Smoothed data file not found at {smoothed_path}"
    with open(smoothed_path, "r") as f:
        lines = f.read().strip().splitlines()
    assert len(lines) == 5000, f"Expected 5000 lines in {smoothed_path}, found {len(lines)}"

def test_svd_results_correct():
    log_path = "/home/user/svd_results.log"
    assert os.path.isfile(log_path), f"SVD results log not found at {log_path}"

    expected_values = [
        "3507.0305",
        "55.4855",
        "52.5028",
        "50.3957",
        "47.3695"
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {log_path}, found {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_values)):
        assert actual == expected, f"Mismatch at line {i+1}: expected {expected}, got {actual}"