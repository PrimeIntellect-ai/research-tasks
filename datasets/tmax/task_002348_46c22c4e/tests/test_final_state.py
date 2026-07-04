# test_final_state.py

import os
import re
import pytest

def test_result_file_exists():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."

def test_result_content_and_metric():
    path = "/home/user/result.txt"
    with open(path, "r") as f:
        content = f.read()

    # Extract Top_ID
    top_id_match = re.search(r"Top_ID:\s*(\S+)", content)
    assert top_id_match is not None, "Could not find 'Top_ID: <Sequence_ID>' in result.txt"
    top_id = top_id_match.group(1)
    assert top_id == "seq4", f"Expected Top_ID to be 'seq4', but got '{top_id}'"

    # Extract Top_Score
    top_score_match = re.search(r"Top_Score:\s*([0-9.]+)", content)
    assert top_score_match is not None, "Could not find 'Top_Score: <Score>' in result.txt"
    try:
        top_score = float(top_score_match.group(1))
    except ValueError:
        pytest.fail(f"Top_Score is not a valid float: {top_score_match.group(1)}")

    # Extract P-value
    p_value_match = re.search(r"P-value:\s*([0-9.]+)", content)
    assert p_value_match is not None, "Could not find 'P-value: <p_value>' in result.txt"
    try:
        p_value = float(p_value_match.group(1))
    except ValueError:
        pytest.fail(f"P-value is not a valid float: {p_value_match.group(1)}")

    # The expected p-value is around 0.02.
    # The threshold is an absolute difference <= 0.05.
    ref_p_value = 0.02
    abs_diff = abs(p_value - ref_p_value)
    assert abs_diff <= 0.05, f"P-value metric failed: agent p-value {p_value} is not within 0.05 of reference {ref_p_value} (difference: {abs_diff})"

def test_detrend_awk_fixed():
    path = "/app/bio-spectral-v1.0/detrend.awk"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check if a small epsilon or addition is present before sqrt
    # The agent might add var = var + 1e-6 or similar
    assert "1e-6" in content or "0.000001" in content or "1e-5" in content or "0.00001" in content, \
        "Could not find a small epsilon (e.g., 1e-6) added to the variance in detrend.awk"