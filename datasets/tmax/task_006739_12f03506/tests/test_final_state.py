# test_final_state.py

import os
import subprocess
import pytest

def get_expected_means():
    cmd = """awk -F, 'NR>1 {print $4}' /home/user/data.csv | awk '
BEGIN { srand(42) }
{ val[NR] = $1 }
END {
  N = NR
  for (iter=1; iter<=1000; iter++) {
    sum = 0
    for (i=1; i<=N; i++) {
        idx = int(rand() * N) + 1
        sum += val[idx]
    }
    printf "%.6f\\n", sum / N
  }
}' | sort -n"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def test_means_txt():
    """Test that means.txt exists and contains the correct reproducible output."""
    file_path = "/home/user/means.txt"
    assert os.path.exists(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        actual_means = f.read().strip().split('\n')

    expected_means = get_expected_means()

    assert len(actual_means) == 1000, f"{file_path} should contain exactly 1000 lines."
    assert actual_means == expected_means, f"The contents of {file_path} do not match the expected reproducible output from awk."

def test_ci_txt():
    """Test that ci.txt exists and contains the correctly formatted 95% confidence interval."""
    file_path = "/home/user/ci.txt"
    assert os.path.exists(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        actual_ci = f.read().strip()

    expected_means = get_expected_means()

    # 25th value (index 24) and 975th value (index 974)
    lower = float(expected_means[24])
    upper = float(expected_means[974])
    expected_ci = f"{lower:.4f},{upper:.4f}"

    assert actual_ci == expected_ci, f"The contents of {file_path} do not match the expected output. Expected '{expected_ci}', got '{actual_ci}'."