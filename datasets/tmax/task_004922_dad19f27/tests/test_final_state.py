# test_final_state.py

import os
import subprocess
import pytest

def test_feature_means_file():
    means_path = "/home/user/feature_means.txt"
    expected_path = "/home/user/expected_means.txt"

    assert os.path.exists(means_path), f"{means_path} does not exist."
    assert os.path.exists(expected_path), f"Truth file {expected_path} is missing."

    with open(means_path, "r") as f:
        student_content = f.read().strip()
    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    student_means = [x.strip() for x in student_content.split(",")]
    expected_means = [x.strip() for x in expected_content.split(",")]

    assert len(student_means) == 4, f"Expected 4 comma-separated means, got {len(student_means)} in {means_path}."

    for s_val, e_val in zip(student_means, expected_means):
        try:
            s_float = float(s_val)
            e_float = float(e_val)
        except ValueError:
            pytest.fail(f"Could not parse mean value as float. Student: '{s_val}', Expected: '{e_val}'")

        assert abs(s_float - e_float) <= 1e-4, \
            f"Mean value {s_float} differs from expected {e_float} by more than 1e-4."

def test_training_features_h5():
    h5_path = "/home/user/training_features.h5"
    assert os.path.exists(h5_path), f"{h5_path} does not exist."

    # We use a subprocess to validate the HDF5 file using the pre-installed h5py,
    # ensuring we only use standard library modules in the pytest suite itself.
    check_script = f"""
import h5py
import sys

try:
    with h5py.File('{h5_path}', 'r') as f:
        if 'features' not in f:
            print("Dataset 'features' is missing in the HDF5 file.")
            sys.exit(1)

        shape = f['features'].shape
        if shape != (1000, 4):
            print(f"Incorrect shape for 'features' dataset: expected (1000, 4), got {{shape}}.")
            sys.exit(1)

        dtype = str(f['features'].dtype)
        if dtype != 'float64':
            print(f"Incorrect dtype for 'features' dataset: expected float64, got {{dtype}}.")
            sys.exit(1)
except Exception as e:
    print(f"Error reading HDF5 file: {{e}}")
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", check_script], capture_output=True, text=True)
    assert result.returncode == 0, f"HDF5 validation failed:\n{result.stdout.strip()}"