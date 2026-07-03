# test_final_state.py

import os
import math
import pytest

def compute_expected_mean():
    # Recompute the expected mean based on the input data
    data_x = {1: 1.5, 2: 2.3, 3: 3.1, 4: 4.0, 5: 5.2, 6: 6.1, 7: 7.0, 8: 8.5, 9: 9.2, 10: 10.1}
    data_y = {3: 2.9, 1: 1.4, 10: 9.9, 5: 5.1, 4: 4.1, 8: 8.3, 2: 2.0, 9: 8.9, 7: 7.2, 6: 5.8}

    p = []
    for i in sorted(data_x.keys()):
        if i in data_y:
            p.append((data_x[i] + data_y[i]) / math.sqrt(2))

    return sum(p) / len(p)

def test_bootstrap_results_file():
    file_path = "/home/user/bootstrap_results.txt"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, found {len(lines)}."

    assert lines[0].startswith("Original Mean:"), "First line must start with 'Original Mean:'"
    assert lines[1].startswith("Bootstrap SE:"), "Second line must start with 'Bootstrap SE:'"

    try:
        actual_mean_str = lines[0].split(":")[1].strip()
        actual_se_str = lines[1].split(":")[1].strip()

        actual_mean = float(actual_mean_str)
        actual_se = float(actual_se_str)
    except ValueError:
        pytest.fail("Could not parse numeric values from the output file.")

    expected_mean = compute_expected_mean()
    expected_mean_str = f"{expected_mean:.6f}"

    # The C++ mt19937 with seed 42 and modulo 10 gives exactly this SE
    expected_se_str = "1.258525"

    assert actual_mean_str == expected_mean_str, f"Expected Original Mean to be {expected_mean_str}, got {actual_mean_str}"
    assert actual_se_str == expected_se_str, f"Expected Bootstrap SE to be {expected_se_str}, got {actual_se_str}"