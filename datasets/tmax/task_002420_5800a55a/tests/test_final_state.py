# test_final_state.py
import os
import math

def p(x):
    return math.exp(-x*x/2.0) / math.sqrt(2.0 * math.pi)

def q(x, nu):
    return math.gamma((nu+1)/2.0) / (math.sqrt(nu * math.pi) * math.gamma(nu/2.0)) * math.pow(1.0 + x*x/nu, -(nu+1)/2.0)

def integrand(x, nu):
    P = p(x)
    Q = q(x, nu)
    return P * math.log((P + 1e-15) / (Q + 1e-15))

def simpsons(nu):
    a = -20.0
    b = 20.0
    N = 100000
    dx = (b - a) / N
    S = integrand(a, nu) + integrand(b, nu)
    for i in range(1, N, 2):
        S += 4.0 * integrand(a + i*dx, nu)
    for i in range(2, N-1, 2):
        S += 2.0 * integrand(a + i*dx, nu)
    return S * dx / 3.0

def test_source_code_exists():
    assert os.path.exists("/home/user/kl_div.cpp"), "/home/user/kl_div.cpp does not exist"

def test_executable_exists():
    assert os.path.exists("/home/user/kl_calc"), "/home/user/kl_calc does not exist"
    assert os.access("/home/user/kl_calc", os.X_OK), "/home/user/kl_calc is not executable"

def test_results_file_and_values():
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"{results_path} does not exist"

    with open(results_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 2, f"Expected exactly 2 lines in {results_path}, found {len(lines)}"

    try:
        kl_val = float(lines[0].strip())
        deriv_val = float(lines[1].strip())
    except ValueError:
        assert False, "Could not parse the outputs as floats"

    # Recompute expected values
    kl_3 = simpsons(3.0)
    kl_301 = simpsons(3.01)
    kl_299 = simpsons(2.99)
    expected_deriv = (kl_301 - kl_299) / 0.02

    # Allow +/- 0.000002 for floating point differences between Python and C++
    assert abs(kl_val - kl_3) <= 2e-6, f"Expected KL divergence to be approx {kl_3:.6f}, got {kl_val}"
    assert abs(deriv_val - expected_deriv) <= 2e-6, f"Expected derivative to be approx {expected_deriv:.6f}, got {deriv_val}"