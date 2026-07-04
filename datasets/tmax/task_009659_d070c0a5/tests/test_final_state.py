# test_final_state.py

import os
import math
import subprocess
import pytest

def solve_ode(y0):
    y = float(y0)
    dt = 0.1
    for _ in range(100):
        y += -0.1 * y * dt
    return y

def test_rust_code_modified():
    main_rs_path = "/home/user/sim_project/src/main.rs"
    assert os.path.isfile(main_rs_path), f"The file {main_rs_path} is missing."

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "rayon" in content, "The Rust code must still use the 'rayon' crate."
    assert "par_iter" in content or "par_bridge" in content or "spawn" in content, "The Rust code must still use parallelization."

def test_results_csv_correct():
    csv_path = "/home/user/results.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5000, f"Expected exactly 5000 results in {csv_path}, found {len(lines)}."

    # Check deterministic order and correct values
    for i in range(5000):
        expected_val = solve_ode(i)
        try:
            actual_val = float(lines[i])
        except ValueError:
            pytest.fail(f"Could not parse line {i+1} as float: {lines[i]}")

        assert math.isclose(actual_val, expected_val, rel_tol=1e-5), \
            f"Value mismatch at line {i+1}. Expected approx {expected_val}, got {actual_val}. Ensure deterministic ordering."

def test_bootstrap_script_exists():
    script_path = "/home/user/bootstrap.py"
    assert os.path.isfile(script_path), f"The file {script_path} is missing."

def test_bootstrap_ci_txt_correct():
    txt_path = "/home/user/bootstrap_ci.txt"
    assert os.path.isfile(txt_path), f"The file {txt_path} is missing."

    with open(txt_path, "r") as f:
        actual_content = f.read().strip()

    # Recompute the expected value using a subprocess to leverage numpy deterministically
    code = """
import numpy as np
def solve_ode(y0):
    y = float(y0)
    dt = 0.1
    for _ in range(100):
        y += -0.1 * y * dt
    return y
results = np.array([solve_ode(i) for i in range(5000)])
np.random.seed(42)
boot_means = []
for _ in range(1000):
    sample = np.random.choice(results, size=len(results), replace=True)
    boot_means.append(np.mean(sample))
lower = np.percentile(boot_means, 2.5)
upper = np.percentile(boot_means, 97.5)
print(f'95% CI: [{lower:.4f}, {upper:.4f}]')
"""
    try:
        proc = subprocess.run(["python3", "-c", code], capture_output=True, text=True, check=True)
        expected_content = proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected CI using numpy: {e.stderr}")

    assert actual_content == expected_content, \
        f"The content of {txt_path} does not match the expected format or value.\nExpected: {expected_content}\nGot: {actual_content}"