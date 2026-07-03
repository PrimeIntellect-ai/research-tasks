# test_final_state.py

import os
import pytest

def compute_expected_max():
    S_map = {'A': 1.0, 'T': 0.8, 'C': 0.5, 'G': 0.2}
    sequences = [
        "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT",
        "AAAAATTTTTCCCCCGGGGGAAAAATTTTTCCCCCGGGGGAAAAATTTTT",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTAC",
        "TCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTC"
    ]

    D = 0.5
    dx = 1.0
    dt = 0.1
    koff = 0.01
    kon = 0.05
    steps = 100
    L = 50

    max_val = 0.0

    for seq in sequences:
        u = [0.0] * L
        S = [S_map.get(base, 0.0) for base in seq]

        for step in range(steps):
            new_u = list(u)
            for i in range(1, L - 1):
                diffusion = D * (u[i-1] - 2*u[i] + u[i+1]) / (dx * dx)
                reaction = -koff * u[i] + kon * S[i]
                new_u[i] = u[i] + dt * (diffusion + reaction)
            u = new_u

        for val in u:
            if val > max_val:
                max_val = val

    return f"Max Concentration: {max_val:.4f}"

def test_files_exist():
    assert os.path.exists("/home/user/simulate.cpp"), "/home/user/simulate.cpp is missing."
    assert os.path.exists("/home/user/analyze.ipynb"), "/home/user/analyze.ipynb is missing."
    assert os.path.exists("/home/user/output.csv"), "/home/user/output.csv is missing."
    assert os.path.exists("/home/user/max_concentration.log"), "/home/user/max_concentration.log is missing."

def test_max_concentration_log():
    log_path = "/home/user/max_concentration.log"
    assert os.path.exists(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = compute_expected_max()
    assert content == expected_content, f"Content of {log_path} is incorrect. Expected '{expected_content}', got '{content}'."