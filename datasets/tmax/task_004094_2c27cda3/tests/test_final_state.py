# test_final_state.py

import os
import subprocess
import time
import random
import pytest

ORACLE_PATH = "/app/integrator_oracle"
FAST_INTEGRATOR_PATH = "/home/user/fast_integrator"
SCRIPT_PATH = "/home/user/test_regression.sh"

def test_files_exist():
    assert os.path.exists(FAST_INTEGRATOR_PATH), f"Optimized executable not found at {FAST_INTEGRATOR_PATH}"
    assert os.access(FAST_INTEGRATOR_PATH, os.X_OK), f"File at {FAST_INTEGRATOR_PATH} is not executable"

    assert os.path.exists(SCRIPT_PATH), f"Bash script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Bash script at {SCRIPT_PATH} is not executable"

def run_binary(binary_path, guess, target_c):
    start_time = time.perf_counter()
    result = subprocess.run(
        [binary_path, str(guess), str(target_c)],
        capture_output=True,
        text=True,
        check=True
    )
    end_time = time.perf_counter()

    # Parse the output as a float. The binary should output the root.
    # We'll just take the last float found in the output to be safe, or just strip it.
    output_str = result.stdout.strip()
    try:
        # If there are multiple lines, assume the result is the last line or just parse it.
        # Often it's just a single number.
        val = float(output_str.split()[-1])
    except ValueError:
        pytest.fail(f"Could not parse output from {binary_path}: {output_str}")

    return val, end_time - start_time

def test_accuracy_and_speedup():
    random.seed(42)

    num_trials = 50
    oracle_times = []
    fast_times = []
    max_error = 0.0

    for _ in range(num_trials):
        guess = random.uniform(0.5, 1.5)
        # The integral of e^{-t^2} from 0 to inf is ~0.886. 
        # Pick C between 0.1 and 0.8 so a root exists.
        target_c = random.uniform(0.1, 0.8)

        oracle_val, oracle_time = run_binary(ORACLE_PATH, guess, target_c)
        fast_val, fast_time = run_binary(FAST_INTEGRATOR_PATH, guess, target_c)

        oracle_times.append(oracle_time)
        fast_times.append(fast_time)

        error = abs(oracle_val - fast_val)
        if error > max_error:
            max_error = error

    mean_oracle_time = sum(oracle_times) / num_trials
    mean_fast_time = sum(fast_times) / num_trials

    speedup = mean_oracle_time / mean_fast_time if mean_fast_time > 0 else float('inf')

    assert max_error <= 1e-6, f"Maximum L_infinity error {max_error} exceeds threshold 1e-6"
    assert speedup >= 2.0, f"Speedup {speedup:.2f}x is below the 2.0x threshold (Oracle: {mean_oracle_time:.4f}s, Fast: {mean_fast_time:.4f}s)"