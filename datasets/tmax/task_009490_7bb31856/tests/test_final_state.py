# test_final_state.py

import os
import re
import pytest

def test_result_summary_exists_and_correct():
    file_path = "/home/user/result_summary.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you write the output?"

    with open(file_path, "r") as f:
        content = f.read()

    # Parse Count
    count_match = re.search(r"Count:\s*(\d+)", content)
    assert count_match is not None, "Could not find 'Count: <integer>' in result_summary.txt. Check your output format."
    count_val = int(count_match.group(1))

    # The expected count based on the deterministically generated dataset is 1215
    assert count_val == 1215, f"Expected Count to be 1215, but got {count_val}."

    # Parse MaxCov
    cov_match = re.search(r"MaxCov:\s*([0-9.]+)", content)
    assert cov_match is not None, "Could not find 'MaxCov: <float>' in result_summary.txt. Check your output format."
    cov_val = float(cov_match.group(1))

    # The expected MaxCov is approximately 0.0090
    assert 0.0088 <= cov_val <= 0.0092, f"Expected MaxCov to be around 0.0090, but got {cov_val}."