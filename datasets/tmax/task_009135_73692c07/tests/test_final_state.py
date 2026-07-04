# test_final_state.py
import os
import math
import pytest

def test_script_exists_and_executable():
    """Verify that the bash script exists and is executable."""
    script_path = "/home/user/run_study.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_log_file_exists():
    """Verify that the output log file exists."""
    log_path = "/home/user/study_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run the script?"

def test_results_correctness():
    """Verify the contents of the study_results.log against expected mathematical values."""
    log_path = "/home/user/study_results.log"
    if not os.path.isfile(log_path):
        pytest.fail("Log file missing.")

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in the log file, found {len(lines)}."

    alpha = 0.1
    expected_Ns = [10, 20, 40]

    # Recompute expected values
    expected_data = {}
    for N in expected_Ns:
        dx = 1.0 / N
        dt_max = (dx**2) / (2 * alpha)
        dt_stable = 0.9 * dt_max
        dt_unstable = 1.1 * dt_max

        M_stable = math.ceil(0.5 / dt_stable)
        t_end_stable = M_stable * dt_stable

        # Run stable
        u_stable = [math.sin(math.pi * i * dx) for i in range(N+1)]
        for _ in range(M_stable):
            u_new = list(u_stable)
            for i in range(1, N):
                u_new[i] = u_stable[i] + (alpha * dt_stable / dx**2) * (u_stable[i+1] - 2*u_stable[i] + u_stable[i-1])
            u_stable = u_new

        mae_stable = 0
        for i in range(1, N):
            x = i * dx
            exact = math.sin(math.pi * x) * math.exp(-math.pi**2 * alpha * t_end_stable)
            mae_stable += abs(u_stable[i] - exact)
        mae_stable /= (N - 1)

        expected_data[N] = {
            'dt_stable': dt_stable,
            'mae_stable': mae_stable,
            'dt_unstable': dt_unstable
        }

    for idx, line in enumerate(lines):
        parts = line.split(',')
        assert len(parts) == 5, f"Line {idx+1} does not have exactly 5 comma-separated values: {line}"

        try:
            N_val = int(parts[0])
            dt_stable_val = float(parts[1])
            mae_stable_val = float(parts[2])
            dt_unstable_val = float(parts[3])
            max_abs_unstable_val = float(parts[4])
        except ValueError:
            pytest.fail(f"Could not parse numerical values from line {idx+1}: {line}")

        assert N_val == expected_Ns[idx], f"Expected N={expected_Ns[idx]} on line {idx+1}, got {N_val}"

        exp = expected_data[N_val]

        # dt values should be exact up to 6 decimal places formatting
        assert math.isclose(dt_stable_val, exp['dt_stable'], abs_tol=1e-5), \
            f"For N={N_val}, expected dt_stable ~ {exp['dt_stable']:.6f}, got {dt_stable_val}"
        assert math.isclose(dt_unstable_val, exp['dt_unstable'], abs_tol=1e-5), \
            f"For N={N_val}, expected dt_unstable ~ {exp['dt_unstable']:.6f}, got {dt_unstable_val}"

        # MAE should be within 1e-4 tolerance
        assert math.isclose(mae_stable_val, exp['mae_stable'], abs_tol=1e-4), \
            f"For N={N_val}, expected MAE_stable ~ {exp['mae_stable']:.6f}, got {mae_stable_val}"

        # Unstable value should indicate blowup (significantly greater than 1.0)
        assert max_abs_unstable_val > 1.0, \
            f"For N={N_val}, max_abs_unstable should be > 1.0 due to blowup, got {max_abs_unstable_val}"