# test_final_state.py

import os
import csv
import pytest

def test_posterior_calculation():
    """Test that the posterior probability is correctly calculated and saved."""
    data_path = '/home/user/data.csv'
    posterior_path = '/home/user/posterior.txt'

    assert os.path.exists(data_path), f"{data_path} does not exist."
    assert os.path.exists(posterior_path), f"{posterior_path} does not exist."

    # Read the data and calculate the expected posterior
    total = 0
    fail_1 = 0
    fail_0 = 0
    temp_7_fail_1 = 0
    temp_7_fail_0 = 0
    vib_4_fail_1 = 0
    vib_4_fail_0 = 0

    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            temp_bin = int(row['temp']) // 10
            vib_bin = int(row['vibration']) // 10
            failure = int(row['failure'])

            if failure == 1:
                fail_1 += 1
                if temp_bin == 7:
                    temp_7_fail_1 += 1
                if vib_bin == 4:
                    vib_4_fail_1 += 1
            elif failure == 0:
                fail_0 += 1
                if temp_bin == 7:
                    temp_7_fail_0 += 1
                if vib_bin == 4:
                    vib_4_fail_0 += 1

    # Calculate probabilities
    p_fail_1 = fail_1 / total
    p_fail_0 = fail_0 / total

    p_temp_7_given_fail_1 = temp_7_fail_1 / fail_1 if fail_1 else 0
    p_temp_7_given_fail_0 = temp_7_fail_0 / fail_0 if fail_0 else 0

    p_vib_4_given_fail_1 = vib_4_fail_1 / fail_1 if fail_1 else 0
    p_vib_4_given_fail_0 = vib_4_fail_0 / fail_0 if fail_0 else 0

    num_1 = p_fail_1 * p_temp_7_given_fail_1 * p_vib_4_given_fail_1
    num_0 = p_fail_0 * p_temp_7_given_fail_0 * p_vib_4_given_fail_0

    posterior = num_1 / (num_1 + num_0)
    expected_val = f"{posterior:.4f}"

    with open(posterior_path, 'r') as f:
        actual_val = f.read().strip()

    assert actual_val == expected_val, f"Expected posterior {expected_val}, but found {actual_val} in {posterior_path}"

def test_benchmark_file():
    """Test that the benchmark file exists and contains a valid positive float."""
    benchmark_path = '/home/user/benchmark.txt'
    assert os.path.exists(benchmark_path), f"{benchmark_path} does not exist."

    with open(benchmark_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {benchmark_path} ('{content}') is not a valid float.")

    assert val >= 0.0, f"Benchmark execution time must be non-negative, got {val}."