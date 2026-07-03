# test_final_state.py
import os
import math

def compute_golden_values():
    N = 1000
    L = 1.0
    dx = L / (N - 1)
    D = 0.01
    r = 1.0
    T = 1.0

    dt = 0.4 * (dx * dx) / D
    steps = math.ceil(T / dt)

    u = [0.0] * N
    for i in range(N // 10):
        u[i] = 1.0

    for _ in range(steps):
        u_new = list(u)
        for i in range(1, N - 1):
            diffusion = D * (u[i+1] - 2*u[i] + u[i-1]) / (dx*dx)
            reaction = r * u[i] * (1 - u[i])
            u_new[i] = u[i] + dt * (diffusion + reaction)
        u = u_new

    x = [i * dx for i in range(N)]

    filtered_x = []
    filtered_u = []
    for i in range(N):
        # Use a small epsilon to match numpy's exact behavior on floating point values
        if 0.2 - 1e-12 <= x[i] <= 0.8 + 1e-12:
            filtered_x.append(x[i])
            filtered_u.append(u[i])

    n = len(filtered_x)
    sum_x = sum(filtered_x)
    sum_y = sum(filtered_u)
    sum_xx = sum(xi * xi for xi in filtered_x)
    sum_xy = sum(xi * yi for xi, yi in zip(filtered_x, filtered_u))

    denominator = n * sum_xx - sum_x * sum_x
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n

    return f"Slope: {slope:.6f}\nIntercept: {intercept:.6f}"

def test_regression_results():
    results_path = "/home/user/regression_results.txt"
    assert os.path.isfile(results_path), f"Missing required output file: {results_path}"

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_content = compute_golden_values().strip()

    assert content == expected_content, (
        f"Contents of {results_path} do not match the expected values.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{content}"
    )

def test_cpp_file_updated():
    cpp_path = "/home/user/fisher_sim.cpp"
    assert os.path.isfile(cpp_path), f"C++ file missing: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "1000" in content, "The C++ file does not seem to have been updated to N=1000."
    assert "omp" in content.lower() or "pragma" in content.lower(), "The C++ file does not seem to contain OpenMP pragmas."