# test_final_state.py

import os
import re

def test_output_file_exists():
    assert os.path.isfile('/home/user/project/output.txt'), "/home/user/project/output.txt does not exist. Did you run the script?"

def test_output_contents():
    with open('/home/user/project/output.txt', 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 2, "output.txt should contain exactly two lines."

    mean_line = content[0].strip()
    opt_line = content[1].strip()

    assert mean_line.startswith("Mean: "), "First line should start with 'Mean: '"
    assert opt_line.startswith("Opt: "), "Second line should start with 'Opt: '"

    try:
        mean_val = float(mean_line.split("Mean: ")[1])
    except ValueError:
        assert False, "Could not parse the mean value as a float."

    try:
        opt_val = float(opt_line.split("Opt: ")[1])
    except ValueError:
        assert False, "Could not parse the opt value as a float."

    # The true mean of 1..100 is 50.5
    # The minimum of x^2 - 50.5 * x is 25.25
    assert abs(mean_val - 50.5) < 1e-4, f"Calculated mean is incorrect. Expected ~50.5000, got {mean_val}"
    assert abs(opt_val - 25.25) < 1e-4, f"Optimized value is incorrect. Expected ~25.2500, got {opt_val}"

def test_output_formatting():
    with open('/home/user/project/output.txt', 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 2, "output.txt should contain exactly two lines."

    mean_match = re.match(r"^Mean: \d+\.\d{4}$", content[0].strip())
    assert mean_match is not None, "Mean output is not formatted to exactly 4 decimal places."

    opt_match = re.match(r"^Opt: \d+\.\d{4}$", content[1].strip())
    assert opt_match is not None, "Opt output is not formatted to exactly 4 decimal places."