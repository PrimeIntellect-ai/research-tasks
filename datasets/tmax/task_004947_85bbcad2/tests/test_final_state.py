# test_final_state.py

import os
import difflib
import pytest

def test_decoded_output_accuracy():
    """
    Check that the decoded output file exists and its content matches the expected
    string 'HELLOWORLD' with a Levenshtein similarity ratio >= 0.9.
    """
    output_file = "/home/user/decoded_output.txt"
    expected = "HELLOWORLD"

    assert os.path.exists(output_file), f"Output file is missing at {output_file}"
    assert os.path.isfile(output_file), f"Path {output_file} is not a file"

    with open(output_file, "r") as f:
        actual = f.read().strip()

    ratio = difflib.SequenceMatcher(None, expected, actual).ratio()

    assert ratio >= 0.9, (
        f"Decoded output does not meet the accuracy threshold. "
        f"Expected at least 0.9, got {ratio:.4f}. "
        f"Expected string: '{expected}', Actual string: '{actual}'"
    )