# test_final_state.py

import os
import math
import pytest

def test_result_file_exists():
    """Test that the result file was generated."""
    assert os.path.isfile("/home/user/result.txt"), "/home/user/result.txt does not exist."

def test_result_accuracy():
    """Test that the computed confidence interval is correct."""
    # Read matrices
    matrices_path = "/home/user/matrices.txt"
    assert os.path.isfile(matrices_path), f"{matrices_path} is missing."

    with open(matrices_path, "r") as f:
        nums = [float(x) for x in f.read().split()]

    assert len(nums) == 1600, "matrices.txt should contain 1600 numbers."

    matrices = []
    for m in range(100):
        mat = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(nums[m * 16 + i * 4 + j])
            mat.append(row)
        matrices.append(mat)

    # Read sequence
    seq_path = "/home/user/sequence.txt"
    assert os.path.isfile(seq_path), f"{seq_path} is missing."

    with open(seq_path, "r") as f:
        seq = f.read().strip()

    base_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    seq_idx = [base_to_idx[b] for b in seq]

    # Calculate log probs
    log_probs = []
    for mat in matrices:
        lp = 0.0
        for i in range(1, len(seq_idx)):
            u = seq_idx[i-1]
            v = seq_idx[i]
            prob = mat[u][v]
            if prob == 0.0:
                lp = -float('inf')
                break
            lp += math.log(prob)
        log_probs.append(lp)

    log_probs.sort()
    expected_lower = log_probs[2]
    expected_upper = log_probs[97]

    expected_str = f"[{expected_lower:.4f}, {expected_upper:.4f}]"

    # Read result
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"{result_path} is missing."

    with open(result_path, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected output '{expected_str}', but got '{actual_str}' in {result_path}."