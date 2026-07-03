# test_final_state.py

import os
import math

def compute_expected_integral(sequence: str) -> float:
    N = len(sequence)
    if N < 2:
        return 0.0

    S = []
    for char in sequence:
        if char in ('G', 'C'):
            S.append(1.0)
        elif char in ('A', 'T'):
            S.append(-1.0)
        else:
            S.append(0.0)

    u = [0.0] * N
    dt = 0.1
    alpha = 0.5

    for _ in range(2):
        u_next = [0.0] * N
        for i in range(1, N - 1):
            laplacian = u[i+1] - 2 * u[i] + u[i-1]
            u_next[i] = u[i] + dt * (alpha * laplacian + S[i])
        u = u_next

    # Trapezoidal rule: dx * ( (u[0] + u[N-1])/2 + sum(u[1...N-2]) )
    # Since u[0] = u[N-1] = 0, it's just the sum of the inner elements.
    integral = sum(u)
    return integral

def test_integral_file_exists():
    """Test that the integral.txt file exists."""
    file_path = "/home/user/integral.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing. Did your C program write the output?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_integral_value():
    """Test that the integral.txt file contains the correct computed value."""
    seq_path = "/home/user/sequence.txt"
    assert os.path.exists(seq_path), f"The file {seq_path} is missing. It should not be deleted."

    with open(seq_path, "r") as f:
        sequence = f.read().strip()

    expected_integral = compute_expected_integral(sequence)
    expected_str = f"{expected_integral:.4f}"

    out_path = "/home/user/integral.txt"
    assert os.path.exists(out_path), f"The output file {out_path} is missing."

    with open(out_path, "r") as f:
        output_content = f.read().strip()

    assert output_content == expected_str, (
        f"Expected integral value '{expected_str}', but got '{output_content}'. "
        "Check your finite-difference implementation, boundary conditions, and trapezoidal rule."
    )