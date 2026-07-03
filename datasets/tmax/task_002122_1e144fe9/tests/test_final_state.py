# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def test_resolve_network_output():
    cpp_file = "/home/user/resolve_network.cpp"
    assert os.path.exists(cpp_file), f"Required file {cpp_file} does not exist."

    exe_path = "/tmp/resolve_network"
    compile_cmd = ["g++", cpp_file, "-o", exe_path]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Compilation failed:\n{compile_res.stderr}"

    run_res = subprocess.run([exe_path], capture_output=True, text=True)
    assert run_res.returncode == 0, f"Execution failed:\n{run_res.stderr}"

    output = run_res.stdout.strip()
    try:
        val = float(output)
    except ValueError:
        pytest.fail(f"Could not parse program output as a float. Output was: {output}")

    # Recompute the expected KL divergence
    # Nodes: 0, 1, 2, 3 (N=4)
    # Edges: (0,1), (1,2), (2,0), (2,3), (3,3)
    P = np.array([
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.5, 0.0, 0.0, 0.5],
        [0.0, 0.0, 0.0, 1.0]
    ])
    alpha = 0.15
    N = 4

    M = (1 - alpha) * P + alpha * (1.0 / N) * np.ones((N, N))

    # Find stationary distribution (left eigenvector for eigenvalue 1)
    evals, evecs = np.linalg.eig(M.T)
    idx = np.argmin(np.abs(evals - 1.0))
    pi = evecs[:, idx].real
    pi = pi / np.sum(pi)

    # Calculate KL divergence D_KL(pi || U)
    expected_kl = np.sum(pi * np.log(pi / (1.0 / N)))

    err = abs(val - expected_kl)
    threshold = 0.05

    assert err <= threshold, (
        f"KL divergence error {err:.5f} exceeds threshold {threshold}. "
        f"Expected approximately {expected_kl:.5f}, but program output {val}."
    )