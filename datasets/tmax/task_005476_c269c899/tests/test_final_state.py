# test_final_state.py

import os
import subprocess
import pytest

def test_processed_csv():
    processed_path = '/home/user/processed.csv'
    assert os.path.isfile(processed_path), f"File not found: {processed_path}"

    with open(processed_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10, f"Expected 10 lines in {processed_path}, got {len(lines)}"

    # Check the first line as a sample
    first_line = lines[0].split(',')
    assert len(first_line) == 3, f"Expected 3 columns, got {len(first_line)}"
    assert float(first_line[0]) == 2.0
    assert float(first_line[1]) == 3.5
    assert float(first_line[2]) == 5.5

def test_main_go_modified():
    go_file = '/home/user/sim/main.go'
    assert os.path.isfile(go_file), f"File not found: {go_file}"

    with open(go_file, 'r') as f:
        content = f.read()

    # Check if a ridge penalty of 1e-3 or 0.001 was added
    has_penalty = "1e-3" in content or "0.001" in content or "1E-3" in content
    assert has_penalty, "Could not find the ridge penalty (1e-3 or 0.001) in main.go"

def test_sim_tool_compiled():
    bin_path = '/home/user/sim/sim_tool'
    assert os.path.isfile(bin_path), f"Compiled binary not found: {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Binary is not executable: {bin_path}"

def test_convergence_result():
    result_path = '/home/user/convergence_result.txt'
    assert os.path.isfile(result_path), f"File not found: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of {result_path} is not an integer: {content}"
    n = int(content)
    assert n >= 1000, f"n should be at least 1000, got {n}"
    assert n % 1000 == 0, f"n should be a multiple of 1000, got {n}"

    bin_path = '/home/user/sim/sim_tool'

    def get_sim_mean(samples):
        result = subprocess.run([bin_path, '-n', str(samples)], capture_output=True, text=True)
        assert result.returncode == 0, f"sim_tool failed for n={samples}"
        return float(result.stdout.strip())

    # Check that for the submitted n, the difference is strictly less than 0.02
    mean_n = get_sim_mean(n)
    diff_n = abs(mean_n - 5.5)
    assert diff_n < 0.02, f"For n={n}, difference {diff_n} is not strictly less than 0.02"

    # Check that for the previous n (n - 1000), the difference is >= 0.02
    if n > 1000:
        prev_n = n - 1000
        mean_prev = get_sim_mean(prev_n)
        diff_prev = abs(mean_prev - 5.5)
        assert diff_prev >= 0.02, f"For n={prev_n}, difference {diff_prev} is already < 0.02, so {n} is not the smallest."