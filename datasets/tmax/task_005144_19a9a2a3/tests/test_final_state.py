# test_final_state.py

import os
import re

def test_analysis_output_exists_and_correct():
    """Check that the analysis_output.txt file exists and contains the correct values."""
    output_file = '/home/user/analysis_output.txt'
    assert os.path.isfile(output_file), f"The file {output_file} does not exist."

    expected = {
        "lambda": 1.4880,
        "A": 2.2220,
        "DKL": 0.0039,
        "alpha": 0.2862
    }

    with open(output_file, 'r') as f:
        text = f.read()

    for key, expected_val in expected.items():
        match = re.search(rf"{key}:\s*([0-9\.]+)", text)
        assert match is not None, f"Missing '{key}' in output file."
        val = float(match.group(1))
        assert abs(val - expected_val) <= 0.0005, f"Value for {key} is {val}, expected {expected_val} (within 0.0005 tolerance)"