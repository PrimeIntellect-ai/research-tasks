# test_final_state.py

import os

def test_generate_compiled():
    exe_path = "/home/user/workspace/generate"
    assert os.path.isfile(exe_path), "Executable 'generate' is missing. Did you compile generate.c?"
    assert os.access(exe_path, os.X_OK), "'generate' is not executable."

def test_input_h5_exists():
    input_path = "/home/user/workspace/input.h5"
    assert os.path.isfile(input_path), "input.h5 is missing. Did you run the compiled 'generate' executable?"

def test_solution_h5_exists():
    solution_path = "/home/user/workspace/solution.h5"
    assert os.path.isfile(solution_path), "solution.h5 is missing. Did you run optimize.py successfully?"

def test_output_txt_content():
    output_path = "/home/user/workspace/output.txt"
    assert os.path.isfile(output_path), "output.txt is missing. Did you extract and save the output?"

    # Recompute the expected result using pure Python standard library
    # A[i][j] = i + j
    # b[i] = i
    n = 10
    A = [[float(i + j) for j in range(n)] for i in range(n)]
    b = [[float(i)] for i in range(n)]

    # A.T
    A_T = [[A[j][i] for j in range(n)] for i in range(n)]

    # A.T @ A
    ATA = [[sum(A_T[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    # Add regularization term: ATA + lambda * I (lambda = 1.0)
    for i in range(n):
        ATA[i][i] += 1.0

    # A.T @ b
    ATb = [[sum(A_T[i][k] * b[k][0] for k in range(n))] for i in range(n)]

    # Invert (ATA + I) using Gauss-Jordan elimination
    AM = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(ATA)]
    for i in range(n):
        pivot = AM[i][i]
        assert pivot != 0, "Zero pivot encountered during matrix inversion."
        for j in range(2 * n):
            AM[i][j] /= pivot
        for k in range(n):
            if k == i: 
                continue
            factor = AM[k][i]
            for j in range(2 * n):
                AM[k][j] -= factor * AM[i][j]
    ATA_inv = [row[n:] for row in AM]

    # x = (ATA + I)^-1 @ A.T @ b
    x = [sum(ATA_inv[i][k] * ATb[k][0] for k in range(n)) for i in range(n)]

    # Format the first 3 elements to 4 decimal places
    expected_str = " ".join(f"{v:.4f}" for v in x[:3])

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_str, f"Content of output.txt is incorrect. Expected '{expected_str}', but got '{content}'."