# test_final_state.py

import os
import itertools
import pytest

def get_max_score_and_perms():
    # We must use stdlib only for the tests, but numpy is installed as part of the task.
    # We can import numpy here since the task required installing it.
    try:
        import numpy as np
    except ImportError:
        pytest.fail("numpy is not installed. The task requires installing numpy.")

    sequence_path = "/home/user/sequence.txt"
    if not os.path.isfile(sequence_path):
        pytest.fail(f"Missing sequence file: {sequence_path}")

    with open(sequence_path, 'r') as f:
        seq = f.read().strip()

    N = len(seq)
    target_idx = int(np.round(N / 3.0))

    max_score = -1.0
    best_perms = []

    for perm in itertools.permutations([1, 2, 3, 4]):
        mapping = {'A': perm[0], 'C': perm[1], 'G': perm[2], 'T': perm[3]}
        num_seq = np.array([mapping.get(base, 0) for base in seq])

        fft_vals = np.abs(np.fft.fft(num_seq))**2
        signal = fft_vals[target_idx]
        noise = np.mean(fft_vals[1:])

        score = signal / noise if noise > 0 else 0

        if score > max_score + 1e-6:
            max_score = score
            best_perms = [perm]
        elif abs(score - max_score) <= 1e-6:
            best_perms.append(perm)

    return max_score, best_perms

def test_best_mapping_exists():
    """Check if the best_mapping.csv file exists."""
    assert os.path.isfile("/home/user/best_mapping.csv"), "Missing required file: /home/user/best_mapping.csv"

def test_optimize_script_exists_and_executable():
    """Check if the optimize.sh script exists and is executable."""
    script_path = "/home/user/optimize.sh"
    assert os.path.isfile(script_path), f"Missing required file: {script_path}"
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_best_mapping_correctness():
    """Check if the best_mapping.csv contains the optimal permutation and correct score."""
    csv_path = "/home/user/best_mapping.csv"
    assert os.path.isfile(csv_path), "Missing required file: /home/user/best_mapping.csv"

    max_score, best_perms = get_max_score_and_perms()

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "The best_mapping.csv file is empty."

    # Check the last line in case they included a header
    last_line = lines[-1]
    parts = last_line.split(',')

    assert len(parts) == 5, f"Expected 5 comma-separated values in best_mapping.csv, but got {len(parts)}."

    try:
        valA = int(parts[0])
        valC = int(parts[1])
        valG = int(parts[2])
        valT = int(parts[3])
        score = float(parts[4])
    except ValueError:
        pytest.fail("Could not parse the values in best_mapping.csv as integers and a float.")

    actual_perm = (valA, valC, valG, valT)

    assert actual_perm in best_perms, f"The permutation {actual_perm} is not one of the optimal permutations."
    assert abs(score - max_score) < 1e-2, f"The score {score} does not match the expected maximum score {max_score}."