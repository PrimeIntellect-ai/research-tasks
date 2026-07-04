# test_final_state.py
import os
import re

def test_result_file_exists_and_correct():
    """Check that result.txt exists and contains the correctly computed integral."""
    result_file = "/home/user/result.txt"
    assert os.path.exists(result_file), f"File {result_file} does not exist. The analysis pipeline may not have run."
    assert os.path.isfile(result_file), f"{result_file} is not a regular file."

    with open(result_file, "r") as f:
        content = f.read().strip()

    # The expected value is approximately 10.9705. 
    # We tolerate small floating-point discrepancies due to linear algebra backends.
    # The output must be formatted to exactly 4 decimal places.
    pattern = r"^10\.970[456]$"
    assert re.match(pattern, content), (
        f"Result '{content}' in {result_file} does not match the expected computed integral. "
        "Expected a value around 10.9705 formatted to exactly 4 decimal places."
    )