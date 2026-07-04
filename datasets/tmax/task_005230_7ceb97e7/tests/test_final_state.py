# test_final_state.py

import os
import subprocess
import pytest

def test_generate_features_exists_and_executable():
    """Check if generate_features exists and is executable."""
    path = "/home/user/ml_data/generate_features"
    assert os.path.isfile(path), f"The executable {path} does not exist."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_run_all_sh_exists_and_executable():
    """Check if run_all.sh exists and is executable."""
    path = "/home/user/ml_data/run_all.sh"
    assert os.path.isfile(path), f"The script {path} does not exist."
    assert os.access(path, os.X_OK), f"The script {path} is not executable."

def test_training_data_csv_content():
    """Verify the contents of training_data.csv match the expected output."""
    csv_path = "/home/user/ml_data/training_data.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected exactly 50 lines in {csv_path}, found {len(lines)}."

    # Recompile the source code to generate ground truth
    c_file = "/home/user/ml_data/network_mc.c"
    assert os.path.isfile(c_file), f"Source file {c_file} is missing."

    test_bin = "/tmp/test_generate_features_truth"
    try:
        subprocess.run(["gcc", "-o", test_bin, c_file, "-lm"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile {c_file} for verification: {e.stderr.decode()}")

    expected_lines = []
    for seed in range(101, 151):
        try:
            result = subprocess.run([test_bin, str(seed)], capture_output=True, text=True, check=True)
            expected_lines.append(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to run compiled binary for seed {seed}: {e.stderr}")

    assert lines == expected_lines, "The contents of training_data.csv do not match the expected output for seeds 101 to 150."