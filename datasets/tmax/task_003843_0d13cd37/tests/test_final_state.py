# test_final_state.py
import os
import math
import pytest

def get_seqs():
    seqs_path = "/home/user/data/seqs.txt"
    assert os.path.isfile(seqs_path), f"File {seqs_path} is missing."
    with open(seqs_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def compute_expected_cov(seqs):
    n = len(seqs)
    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            score = 0.0
            min_len = min(len(seqs[i]), len(seqs[j]))
            for k in range(min_len):
                if seqs[i][k] == seqs[j][k]:
                    score += 1.0
            if i == j:
                score += 10.0
            mat[i][j] = score
    return mat

def compute_cholesky(A):
    n = len(A)
    L = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - s
                assert val > 0, "Matrix is not positive definite"
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j] - s) / L[j][j]
    return L

def compute_integral(seq):
    mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
    vals = [mapping.get(c, 0) for c in seq]
    if not vals:
        return 0.0
    if len(vals) == 1:
        return 0.0

    integral = 0.0
    for i in range(len(vals) - 1):
        integral += 0.5 * (vals[i] + vals[i+1])
    return integral

def test_executable_compiled():
    exe_path = "/home/user/bin/seq_cov"
    assert os.path.isfile(exe_path), f"Executable {exe_path} not found. Did you compile it?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_cov_txt():
    cov_path = "/home/user/output/cov.txt"
    assert os.path.isfile(cov_path), f"Output file {cov_path} not found."

    seqs = get_seqs()
    expected_mat = compute_expected_cov(seqs)

    with open(cov_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_mat), f"Expected {len(expected_mat)} rows in cov.txt, got {len(lines)}"

    for i, line in enumerate(lines):
        vals = [float(x) for x in line.split()]
        assert len(vals) == len(expected_mat[i]), f"Expected {len(expected_mat[i])} columns in row {i+1}, got {len(vals)}"
        for j, val in enumerate(vals):
            assert math.isclose(val, expected_mat[i][j], abs_tol=1e-3), f"Mismatch at ({i}, {j}): expected {expected_mat[i][j]}, got {val}"

def test_cholesky_output():
    l_path = "/home/user/output/L_matrix.txt"
    assert os.path.isfile(l_path), f"Output file {l_path} not found."

    seqs = get_seqs()
    cov_mat = compute_expected_cov(seqs)
    expected_L = compute_cholesky(cov_mat)

    with open(l_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_L), f"Expected {len(expected_L)} rows in L_matrix.txt, got {len(lines)}"

    for i, line in enumerate(lines):
        # ensure it's space separated and exactly formatted
        parts = line.split()
        assert len(parts) == len(expected_L[i]), f"Expected {len(expected_L[i])} columns in row {i+1}, got {len(parts)}"
        for j, part in enumerate(parts):
            # check 4 decimal places format roughly
            assert "." in part and len(part.split(".")[1]) == 4, f"Value {part} not formatted to 4 decimal places."
            val = float(part)
            assert math.isclose(val, expected_L[i][j], abs_tol=1e-3), f"Mismatch at ({i}, {j}): expected {expected_L[i][j]:.4f}, got {val}"

def test_integrals_output():
    int_path = "/home/user/output/integrals.txt"
    assert os.path.isfile(int_path), f"Output file {int_path} not found."

    seqs = get_seqs()
    expected_integrals = [compute_integral(s) for s in seqs]

    with open(int_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_integrals), f"Expected {len(expected_integrals)} lines in integrals.txt, got {len(lines)}"

    for i, line in enumerate(lines):
        assert "." in line and len(line.split(".")[1]) == 1, f"Value {line} not formatted to 1 decimal place."
        val = float(line)
        assert math.isclose(val, expected_integrals[i], abs_tol=1e-3), f"Mismatch at sequence {i+1}: expected {expected_integrals[i]:.1f}, got {val}"

def test_scripts_exist():
    awk_script = "/home/user/scripts/cholesky.awk"
    bash_script = "/home/user/scripts/integrate.sh"

    assert os.path.isfile(awk_script), f"AWK script {awk_script} not found."
    assert os.path.isfile(bash_script), f"Bash script {bash_script} not found."