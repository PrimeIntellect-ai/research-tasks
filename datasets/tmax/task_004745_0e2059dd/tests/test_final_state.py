# test_final_state.py

import os
import re
import math
import pytest

def test_results_txt_exists():
    assert os.path.isfile("/home/user/results.txt"), "/home/user/results.txt does not exist."

def test_posterior_mean_correct():
    with open("/home/user/results.txt", "r") as f:
        content = f.read()

    match = re.search(r"Posterior Mean:\s*([0-9.]+)", content)
    assert match is not None, "Could not find 'Posterior Mean: <value>' in results.txt."

    post_mean = float(match.group(1))

    # Calculate expected posterior mean from data.csv
    assert os.path.isfile("/home/user/data.csv"), "data.csv is missing."
    with open("/home/user/data.csv", "r") as f:
        data = [int(line.strip()) for line in f if line.strip()]

    assert len(data) == 100, "data.csv should have 100 values."

    orig_mean = sum(data) / 100.0
    expected_post_mean = (50.0 / 25.0 + 100 * orig_mean / 100.0) / (1.0 / 25.0 + 100 / 100.0)

    assert math.isclose(post_mean, expected_post_mean, abs_tol=0.002), \
        f"Expected Posterior Mean to be ~{expected_post_mean:.3f}, but found {post_mean:.3f}."

def test_bootstrap_ci_not_truncated():
    with open("/home/user/results.txt", "r") as f:
        content = f.read()

    match = re.search(r"Bootstrap 95% CI:\s*\[([0-9.]+),\s*([0-9.]+)\]", content)
    assert match is not None, "Could not find 'Bootstrap 95% CI: [lower, upper]' in results.txt."

    lower_bound = match.group(1)
    upper_bound = match.group(2)

    assert "." in lower_bound and "." in upper_bound, "CI bounds must be floats."

    # Check that they are not just integers disguised as floats (e.g. 52.000)
    # The probability of both bounds ending in exactly .000 by chance with continuous division is very low.
    lower_frac = lower_bound.split(".")[1]
    upper_frac = upper_bound.split(".")[1]

    assert lower_frac != "000" or upper_frac != "000", \
        "CI bounds end in .000, which indicates the integer division bug is likely still present."

def test_c_code_fixed():
    c_path = "/home/user/stats_calc.c"
    assert os.path.isfile(c_path), f"File {c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    # The exact buggy line was `boot_means[i] = sum / N;`
    # We should ensure the bug is fixed.
    assert re.search(r"boot_means\[i\]\s*=\s*sum\s*/\s*N\s*;", content) is None, \
        "The integer division bug 'sum / N' is still present in stats_calc.c."

    # Ensure it's compiled
    assert os.path.isfile("/home/user/stats_calc"), "The compiled binary stats_calc is missing."
    assert os.access("/home/user/stats_calc", os.X_OK), "The compiled stats_calc is not executable."