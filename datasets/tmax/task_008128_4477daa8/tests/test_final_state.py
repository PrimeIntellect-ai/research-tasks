# test_final_state.py
import os
import pytest

def compute_expected():
    # We must use numpy to reproduce the exact random sequence requested by the prompt
    import numpy as np

    def test_dt(dt):
        np.random.seed(42)
        N = 10000
        T = 2.0
        steps = int(T / dt)

        X = np.random.randn(N)

        for _ in range(steps):
            Z = np.random.randn(N)
            X = X + (-X**3 + 2*X)*dt + np.sqrt(dt) * Z

        diverged = np.isnan(X).any() or np.isinf(X).any() or (np.abs(X) > 1000.0).any()
        return diverged, X

    for dt in [0.1, 0.05, 0.025, 0.01, 0.005, 0.001]:
        diverged, X = test_dt(dt)
        if not diverged:
            return dt, np.mean(X)
    return None, None

def test_vectorized_sim_exists():
    path = '/home/user/vectorized_sim.py'
    assert os.path.isfile(path), f"The file {path} does not exist. Please save your vectorized code there."

def test_report_content():
    report_path = '/home/user/report.txt'
    assert os.path.isfile(report_path), f"The file {report_path} does not exist."

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, f"The file {report_path} must contain at least two non-empty lines."

    expected_dt, expected_mean = compute_expected()

    # Check first line for optimal dt
    assert str(expected_dt) in lines[0], (
        f"The first line of {report_path} is incorrect. "
        f"Expected to find the optimal dt '{expected_dt}', but got: '{lines[0]}'."
    )

    # Check second line for mean rounded to 4 decimal places
    expected_mean_str = f"{expected_mean:.4f}"
    assert expected_mean_str in lines[1], (
        f"The second line of {report_path} is incorrect. "
        f"Expected to find the mean '{expected_mean_str}', but got: '{lines[1]}'."
    )