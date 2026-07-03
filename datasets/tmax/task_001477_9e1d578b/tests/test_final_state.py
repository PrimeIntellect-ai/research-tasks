# test_final_state.py

import os
import re
import pytest

def test_results_file_exists():
    """Check if the results.txt file exists."""
    file_path = '/home/user/results.txt'
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_results_file_content():
    """Verify the content of results.txt matches the expected format and values."""
    file_path = '/home/user/results.txt'
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # The format should be: T-statistic: [t_val], P-value: [p_val]
    pattern = r"^T-statistic:\s*(-?\d+\.\d{4}),\s*P-value:\s*(\d+\.\d{4})$"
    match = re.match(pattern, content)

    assert match is not None, (
        f"The content of {file_path} does not match the required format. "
        f"Expected 'T-statistic: [t_val], P-value: [p_val]' with 4 decimal places. "
        f"Got: '{content}'"
    )

    t_val = float(match.group(1))
    p_val = float(match.group(2))

    # Expected values based on the fixed seed 42 setup
    expected_t = 33.3742
    expected_p = 0.0000

    assert abs(t_val - expected_t) < 0.01, f"Expected T-statistic around {expected_t}, but got {t_val}."
    assert abs(p_val - expected_p) < 0.0001, f"Expected P-value around {expected_p}, but got {p_val}."