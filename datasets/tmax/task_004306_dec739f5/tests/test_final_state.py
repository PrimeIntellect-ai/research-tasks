# test_final_state.py

import os
import re

def test_stats_txt_exists_and_content():
    stats_path = "/home/user/stats.txt"
    assert os.path.isfile(stats_path), f"File not found: {stats_path}"

    with open(stats_path, "r") as f:
        content = f.read().strip()

    # Expected values based on the initial data:
    # Mean: 8.67
    # Variance: 6.22
    # Max_Abs_Diff: 4.00

    expected_mean = 8.67
    expected_variance = 6.22
    expected_max_abs_diff = 4.00

    # Extract values using regex to handle minor formatting differences
    mean_match = re.search(r"Mean:\s*([0-9.]+)", content)
    var_match = re.search(r"Variance:\s*([0-9.]+)", content)
    diff_match = re.search(r"Max_Abs_Diff:\s*([0-9.]+)", content)

    assert mean_match, "Could not find 'Mean: <value>' in stats.txt"
    assert var_match, "Could not find 'Variance: <value>' in stats.txt"
    assert diff_match, "Could not find 'Max_Abs_Diff: <value>' in stats.txt"

    actual_mean = float(mean_match.group(1))
    actual_var = float(var_match.group(1))
    actual_diff = float(diff_match.group(1))

    assert abs(actual_mean - expected_mean) < 0.015, f"Expected Mean ~ {expected_mean}, got {actual_mean}"
    assert abs(actual_var - expected_variance) < 0.015, f"Expected Variance ~ {expected_variance}, got {actual_var}"
    assert abs(actual_diff - expected_max_abs_diff) < 0.015, f"Expected Max_Abs_Diff ~ {expected_max_abs_diff}, got {actual_diff}"

def test_c_source_code_exists():
    c_path = "/home/user/process.c"
    assert os.path.isfile(c_path), f"C source file not found at {c_path}"