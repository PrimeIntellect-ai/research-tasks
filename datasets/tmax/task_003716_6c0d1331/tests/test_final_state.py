# test_final_state.py
import os
import math

def test_cpp_source_fixed():
    cpp_file = '/home/user/src/nmf_solver.cpp'
    assert os.path.isfile(cpp_file), f"Missing {cpp_file}"
    with open(cpp_file, 'r') as f:
        content = f.read()
    assert "1e-9" in content, "The C++ source code does not seem to include the '1e-9' regularization term."

def test_executable_exists():
    exe_file = '/home/user/nmf_solver'
    assert os.path.isfile(exe_file), f"Missing executable {exe_file}"
    assert os.access(exe_file, os.X_OK), f"{exe_file} is not executable"

def load_matrix(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                matrix.append([float(x) for x in parts])
    return matrix

def test_factorization_outputs():
    w_file = '/home/user/W.txt'
    h_file = '/home/user/H.txt'
    assert os.path.isfile(w_file), f"Missing {w_file}"
    assert os.path.isfile(h_file), f"Missing {h_file}"

    W = load_matrix(w_file)
    H = load_matrix(h_file)

    for row in W:
        for val in row:
            assert not math.isnan(val), "W matrix contains NaN"
            assert not math.isinf(val), "W matrix contains Inf"

    for row in H:
        for val in row:
            assert not math.isnan(val), "H matrix contains NaN"
            assert not math.isinf(val), "H matrix contains Inf"

def test_evaluation_script_and_output():
    eval_script = '/home/user/evaluate.py'
    kl_file = '/home/user/kl_divergence.txt'

    assert os.path.isfile(eval_script), f"Missing {eval_script}"
    assert os.path.isfile(kl_file), f"Missing {kl_file}"

    with open(kl_file, 'r') as f:
        content = f.read().strip()

    try:
        kl_val = float(content)
    except ValueError:
        assert False, f"{kl_file} does not contain a valid float"

    assert not math.isnan(kl_val), "KL divergence is NaN"
    assert kl_val >= 0, "KL divergence must be non-negative"

    # Verify the KL divergence computation
    V = load_matrix('/home/user/data/input_matrix.txt')
    W = load_matrix('/home/user/W.txt')
    H = load_matrix('/home/user/H.txt')

    n = len(V)
    m = len(V[0])
    rank = len(W[0])

    V_approx = [[0.0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(rank):
                V_approx[i][j] += W[i][k] * H[k][j]

    # Flatten
    V_flat = [val for row in V for val in row]
    V_approx_flat = [val for row in V_approx for val in row]

    sum_V = sum(V_flat)
    sum_V_approx = sum(V_approx_flat)

    P = [x / sum_V for x in V_flat]
    Q = [x / sum_V_approx for x in V_approx_flat]

    expected_kl = 0.0
    for p, q in zip(P, Q):
        if p > 0 and q > 0:
            expected_kl += p * math.log(p / q)

    assert math.isclose(kl_val, expected_kl, rel_tol=1e-3, abs_tol=1e-5), \
        f"KL divergence in {kl_file} ({kl_val}) does not match expected value ({expected_kl})"