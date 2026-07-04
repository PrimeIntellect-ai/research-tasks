# test_final_state.py

import os
import statistics
import pytest

def test_fixed_results_exists_and_correct():
    results_file = "/home/user/fixed_results.txt"
    assert os.path.isfile(results_file), f"File {results_file} is missing. Did you save the output?"

    directory = "/home/user/transactions"
    assert os.path.isdir(directory), f"Directory {directory} is missing."

    expected_lines = []
    for f in sorted(os.listdir(directory)):
        if f.endswith('.csv'):
            with open(os.path.join(directory, f)) as file:
                values = [float(line.strip()) for line in file if line.strip()]
                if len(values) > 1:
                    std_dev = statistics.stdev(values)
                else:
                    std_dev = 0.0
                expected_lines.append(f"{f},{std_dev:.4f}")

    with open(results_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {results_file} are incorrect.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{actual_lines}"
    )