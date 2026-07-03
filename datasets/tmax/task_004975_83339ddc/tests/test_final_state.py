# test_final_state.py

import os
import math
import pytest

def test_samples_csv_exists_and_format():
    samples_path = "/home/user/samples.csv"
    assert os.path.exists(samples_path), f"File {samples_path} is missing. Did you save the samples?"

    with open(samples_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10000, f"Expected exactly 10,000 samples, found {len(lines)}."

    for i, line in enumerate(lines):
        cols = line.split(',')
        assert len(cols) == 3, f"Expected 3 columns on line {i+1}, found {len(cols)}."
        try:
            [float(val) for val in cols]
        except ValueError:
            pytest.fail(f"Could not parse values as floats on line {i+1}: {line}")

def test_mcmc_empirical_mean():
    samples_path = "/home/user/samples.csv"
    mean_path = "/tmp/theoretical_mean.txt"

    assert os.path.exists(samples_path), f"File {samples_path} is missing."
    assert os.path.exists(mean_path), f"File {mean_path} is missing."

    with open(mean_path, "r") as f:
        content = f.read().strip()

    theoretical_mean = [float(x) for x in content.split(',')]
    assert len(theoretical_mean) == 3, "Theoretical mean should have 3 components."

    with open(samples_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10000, "Expected exactly 10,000 samples."

    sum_b1, sum_b2, sum_b3 = 0.0, 0.0, 0.0
    for line in lines:
        cols = line.split(',')
        sum_b1 += float(cols[0])
        sum_b2 += float(cols[1])
        sum_b3 += float(cols[2])

    N = len(lines)
    empirical_mean = [sum_b1 / N, sum_b2 / N, sum_b3 / N]

    # Calculate L2 distance
    l2_distance = math.sqrt(sum((e - t) ** 2 for e, t in zip(empirical_mean, theoretical_mean)))

    assert l2_distance < 0.1, (
        f"L2 distance between empirical mean {empirical_mean} and "
        f"theoretical mean {theoretical_mean} is {l2_distance:.4f}, which is >= 0.1. "
        "The MCMC sampler may not be correctly implemented or hasn't converged."
    )