# test_final_state.py
import os
import math

def test_rust_project_exists():
    cargo_toml = "/home/user/repro_check/Cargo.toml"
    assert os.path.exists(cargo_toml), f"Rust Cargo project not found at {cargo_toml}. Did you create the project?"

def test_validation_log_exists():
    log_path = "/home/user/validation_log.txt"
    assert os.path.exists(log_path), f"Validation log not found at {log_path}."

def test_validation_log_content():
    run1_path = "/home/user/run1.txt"
    run2_path = "/home/user/run2.txt"

    # Read the original files to compute the expected truth dynamically
    with open(run1_path, "r") as f1:
        lines1 = [float(x) for x in f1.read().splitlines() if x.strip()]
    with open(run2_path, "r") as f2:
        lines2 = [float(x) for x in f2.read().splitlines() if x.strip()]

    n = len(lines1)
    assert n > 1, "Not enough lines to compute standard deviation."

    # Compute differences
    diffs = [l1 - l2 for l1, l2 in zip(lines1, lines2)]

    # Calculate mean
    mean_diff = sum(diffs) / n

    # Calculate sample variance (N-1) and standard deviation
    variance = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
    std_dev = math.sqrt(variance)

    # Calculate margin of error with Z = 1.96
    margin_error = 1.96 * (std_dev / math.sqrt(n))

    ci_lower = mean_diff - margin_error
    ci_upper = mean_diff + margin_error

    # Format exactly to 4 decimal places
    expected_line = f"MEAN_DIFF: {mean_diff:.4f}, CI_LOWER: {ci_lower:.4f}, CI_UPPER: {ci_upper:.4f}"

    log_path = "/home/user/validation_log.txt"
    with open(log_path, "r") as f:
        log_content = f.read()

    assert expected_line in log_content, (
        f"Expected to find the exact string:\n'{expected_line}'\n"
        f"in {log_path}, but it was not found. Current content:\n{log_content}"
    )