# test_final_state.py

import os
import re
import pytest

def test_ci_file_exists_and_format():
    ci_path = '/home/user/ci.txt'
    assert os.path.isfile(ci_path), f"File {ci_path} is missing."

    with open(ci_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, f"Expected at least 2 lines in {ci_path}, got {len(content)}."

    k_line = content[0].strip()
    c_line = content[1].strip()

    # Check format: k: [lower, upper] with 3 decimal places
    k_match = re.match(r'^k:\s*\[(-?\d+\.\d{3}),\s*(-?\d+\.\d{3})\]$', k_line)
    assert k_match is not None, f"Line 1 format incorrect. Expected 'k: [lower, upper]' with 3 decimal places, got: '{k_line}'"

    c_match = re.match(r'^c:\s*\[(-?\d+\.\d{3}),\s*(-?\d+\.\d{3})\]$', c_line)
    assert c_match is not None, f"Line 2 format incorrect. Expected 'c: [lower, upper]' with 3 decimal places, got: '{c_line}'"

    k_lower, k_upper = float(k_match.group(1)), float(k_match.group(2))
    c_lower, c_upper = float(c_match.group(1)), float(c_match.group(2))

    assert k_lower < k_upper, "k lower bound must be less than upper bound"
    assert c_lower < c_upper, "c lower bound must be less than upper bound"

def test_plot_file_exists():
    plot_path = '/home/user/fit_plot.png'
    assert os.path.isfile(plot_path), f"Plot file {plot_path} is missing."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."