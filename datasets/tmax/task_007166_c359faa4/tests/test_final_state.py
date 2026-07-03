# test_final_state.py

import os
import struct
import math
import pytest

def test_solution_file_exists_and_correct():
    solution_file = "/home/user/solution.txt"
    bin_file = "/home/user/uptime_stats/data/latencies.bin"

    assert os.path.isfile(bin_file), f"Data file {bin_file} is missing."
    assert os.path.isfile(solution_file), f"Solution file {solution_file} is missing."

    # Compute ground truth mathematically from the binary file
    with open(bin_file, "rb") as f:
        data = f.read()

    n = len(data) // 4
    assert n > 0, "Binary data file is empty."

    # Read as f32
    floats = struct.unpack(f"<{n}f", data)

    # Accumulate using Python's fsum which tracks partial sums for high precision
    total = math.fsum(floats)
    mean = total / n

    # Two-pass variance for high precision
    var_sum = math.fsum((x - mean) ** 2 for x in floats)
    variance = var_sum / n

    expected_mean_str = f"{mean:.4f}"
    expected_variance_str = f"{variance:.4f}"

    # Read and parse student's solution
    with open(solution_file, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]
    assert len(lines) >= 2, "solution.txt must contain at least two lines for Mean and Variance."

    mean_line = lines[0]
    var_line = lines[1]

    assert mean_line.startswith("Mean:"), "First line must start with 'Mean:'"
    assert var_line.startswith("Variance:"), "Second line must start with 'Variance:'"

    actual_mean_str = mean_line.split(":", 1)[1].strip()
    actual_variance_str = var_line.split(":", 1)[1].strip()

    assert actual_mean_str == expected_mean_str, (
        f"Mean is incorrect. Expected {expected_mean_str}, got {actual_mean_str}. "
        "Check precision loss or missing data points."
    )

    assert actual_variance_str == expected_variance_str, (
        f"Variance is incorrect. Expected {expected_variance_str}, got {actual_variance_str}. "
        "Check for numerical instability or missing data points."
    )