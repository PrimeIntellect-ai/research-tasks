# test_final_state.py

import os
import subprocess

def test_venv_and_packages():
    venv_dir = "/home/user/venv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."

    python_exec = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_exec), f"Python executable not found at {python_exec}."

    # Check if numpy is installed
    result = subprocess.run([python_exec, "-c", "import numpy"], capture_output=True)
    assert result.returncode == 0, "numpy is not installed in the virtual environment."

    # Check if scipy is installed
    result = subprocess.run([python_exec, "-c", "import scipy"], capture_output=True)
    assert result.returncode == 0, "scipy is not installed in the virtual environment."

def test_features_csv_content():
    csv_path = "/home/user/features.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Sequence_ID,Total_Energy",
        "Protein_A,1497.00",
        "Protein_B,1263.29",
        "Protein_C,1486.20"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)} in {csv_path}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."