# test_final_state.py

import os
import re
import pytest

def test_analyze_script_exists():
    """Check if the analyze.py script was created."""
    script_path = "/home/user/analyze.py"
    assert os.path.isfile(script_path), f"Script file is missing at {script_path}"

def test_ci_output_exists():
    """Check if the ci.txt output file was created."""
    output_path = "/home/user/ci.txt"
    assert os.path.isfile(output_path), f"Output file is missing at {output_path}"

def test_ci_output_format_and_values():
    """Check if the ci.txt output file has the correct format and values."""
    output_path = "/home/user/ci.txt"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    # Check format: [lower, upper]
    match = re.match(r'^\[([0-9.]+),\s*([0-9.]+)\]$', content)
    assert match is not None, f"Output format in {output_path} is incorrect. Expected format '[lower, upper]', got '{content}'"

    lower_str, upper_str = match.groups()

    # Check if they have 3 decimal places
    assert len(lower_str.split('.')[-1]) == 3, f"Lower bound should have exactly 3 decimal places, got {lower_str}"
    assert len(upper_str.split('.')[-1]) == 3, f"Upper bound should have exactly 3 decimal places, got {upper_str}"

    lower = float(lower_str)
    upper = float(upper_str)

    expected_lower = 0.787
    expected_upper = 0.913

    # Check values with a tolerance of 0.005
    assert abs(lower - expected_lower) <= 0.005, f"Lower bound {lower} is not within tolerance of expected {expected_lower}"
    assert abs(upper - expected_upper) <= 0.005, f"Upper bound {upper} is not within tolerance of expected {expected_upper}"