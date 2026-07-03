# test_final_state.py
import os

def read_results(path):
    with open(path, 'r') as f:
        content = f.read().strip()
        if not content:
            return []
        return [float(x) for x in content.split(',')]

def test_fit_model_c_exists():
    """Check if the C program source file exists."""
    assert os.path.isfile("/home/user/fit_model.c"), "C program /home/user/fit_model.c is missing."

def test_analytical_results():
    """Check if analytical results are correct and match the expected OLS solution."""
    path = "/home/user/analytical_results.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    try:
        vals = read_results(path)
    except ValueError:
        assert False, f"Could not parse floats from {path}. Ensure it is comma-separated."

    assert len(vals) == 3, f"Expected 3 values in {path}, got {len(vals)}."

    expected = [2.441, 1.189, -0.765]
    for v, e in zip(vals, expected):
        assert abs(v - e) <= 0.015, f"Analytical result {v} differs from expected {e} by more than allowed tolerance."

def test_mcmc_results():
    """Check if MCMC results exist and have converged close to the analytical solution."""
    path_mcmc = "/home/user/mcmc_results.txt"
    path_anal = "/home/user/analytical_results.txt"

    assert os.path.isfile(path_mcmc), f"File {path_mcmc} is missing."
    if not os.path.isfile(path_anal):
        return # Handled by previous test

    try:
        mcmc_vals = read_results(path_mcmc)
        anal_vals = read_results(path_anal)
    except ValueError:
        assert False, f"Could not parse floats from results files."

    assert len(mcmc_vals) == 3, f"Expected 3 values in {path_mcmc}, got {len(mcmc_vals)}."

    for m, a in zip(mcmc_vals, anal_vals):
        assert abs(m - a) <= 0.05, f"MCMC result {m} differs from analytical {a} by more than 0.05. MCMC did not converge sufficiently."