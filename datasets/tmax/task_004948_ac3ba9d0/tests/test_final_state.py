# test_final_state.py
import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/analyze_spectra"
    assert os.path.isfile(executable_path), f"Executable {executable_path} was not found. Did you compile the C++ program?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_result_file_contents():
    result_path = "/home/user/result.txt"
    data_path = "/home/user/data.csv"
    ref_path = "/home/user/reference.txt"

    assert os.path.isfile(result_path), f"Result file {result_path} was not created."
    assert os.path.isfile(data_path), f"Data file {data_path} is missing."
    assert os.path.isfile(ref_path), f"Reference file {ref_path} is missing."

    # Compute expected values dynamically
    with open(data_path, 'r') as f:
        lines = f.read().strip().split('\n')

    # skip header
    freqs = []
    psds = []
    for line in lines[1:]:
        if not line.strip():
            continue
        f_val, p_val = line.split(',')
        freqs.append(float(f_val))
        psds.append(float(p_val))

    expected_energy = 0.0
    for i in range(len(freqs) - 1):
        dx = freqs[i+1] - freqs[i]
        expected_energy += 0.5 * dx * (psds[i] + psds[i+1])

    with open(ref_path, 'r') as f:
        ref_energy = float(f.read().strip())

    expected_exceeds = "Yes" if expected_energy > ref_energy else "No"

    # Read actual results
    with open(result_path, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(actual_lines) == 2, f"Expected exactly 2 lines in {result_path}, but got {len(actual_lines)}."

    expected_line1 = f"Total Energy: {expected_energy:.2f}"
    expected_line2 = f"Exceeds Reference: {expected_exceeds}"

    assert actual_lines[0] == expected_line1, f"First line mismatch. Expected: '{expected_line1}', Got: '{actual_lines[0]}'"
    assert actual_lines[1] == expected_line2, f"Second line mismatch. Expected: '{expected_line2}', Got: '{actual_lines[1]}'"