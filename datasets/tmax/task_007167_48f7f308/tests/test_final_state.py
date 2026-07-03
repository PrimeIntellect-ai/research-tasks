# test_final_state.py
import os
import random
import pytest

def test_profile_sh_exists_and_executable():
    script_path = "/home/user/profile.sh"
    assert os.path.exists(script_path), f"File {script_path} is missing."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_runtimes_txt_valid():
    runtimes_path = "/home/user/runtimes.txt"
    assert os.path.exists(runtimes_path), f"File {runtimes_path} is missing."

    with open(runtimes_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 30, f"runtimes.txt should have exactly 30 entries, found {len(lines)}."

    for idx, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line {idx+1} in runtimes.txt is not a valid float: {line}")

def test_ci_output_valid():
    ci_path = "/home/user/ci_output.txt"
    assert os.path.exists(ci_path), f"File {ci_path} is missing."

    with open(ci_path, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 2, f"ci_output.txt must be in format lower_bound,upper_bound. Got: {content}"

    try:
        lower = float(parts[0])
        upper = float(parts[1])
    except ValueError:
        pytest.fail(f"ci_output.txt contains invalid floats: {content}")

    assert lower <= upper, "Lower bound must be less than or equal to upper bound."

def test_bootstrap_logic():
    runtimes_path = "/home/user/runtimes.txt"
    ci_path = "/home/user/ci_output.txt"

    if not os.path.exists(runtimes_path) or not os.path.exists(ci_path):
        pytest.skip("Required files missing, cannot verify bootstrap logic.")

    with open(runtimes_path, "r") as f:
        runtimes = [float(line.strip()) for line in f.readlines() if line.strip()]

    with open(ci_path, "r") as f:
        content = f.read().strip()
        parts = content.split(",")
        try:
            lower = float(parts[0])
            upper = float(parts[1])
        except ValueError:
            pytest.skip("ci_output.txt format is invalid, skipping bootstrap logic check.")

    # Calculate true bootstrap CI from the agent's runtimes
    random.seed(42)
    means = []
    n = len(runtimes)
    for _ in range(10000):
        sample = [random.choice(runtimes) for _ in range(n)]
        means.append(sum(sample) / n)

    means.sort()

    # Percentile calculation
    def percentile(data, p):
        k = (len(data) - 1) * p
        f = int(k)
        c = f + 1
        if f == c or c >= len(data):
            return data[f]
        return data[f] + (k - f) * (data[c] - data[f])

    true_lower = percentile(means, 0.025)
    true_upper = percentile(means, 0.975)

    assert abs(lower - true_lower) <= 0.05, f"Lower bound {lower} differs from expected {true_lower:.3f} by > 0.05"
    assert abs(upper - true_upper) <= 0.05, f"Upper bound {upper} differs from expected {true_upper:.3f} by > 0.05"