# test_final_state.py

import os
import difflib
import pytest

def test_token_extraction_accuracy():
    target_file = "/home/user/token.txt"

    # Check if the target file exists
    assert os.path.isfile(target_file), f"Output file {target_file} does not exist."

    # Read the extracted token
    with open(target_file, "r") as f:
        extracted_token = f.read().strip()

    # The ground truth reference token
    reference_token = "SEC{0x4F}"

    # Calculate the string similarity using SequenceMatcher
    ratio = difflib.SequenceMatcher(None, reference_token, extracted_token).ratio()

    # Assert the metric against the threshold
    threshold = 1.0
    assert ratio >= threshold, (
        f"Token extraction accuracy too low. "
        f"Expected ratio >= {threshold}, but got {ratio}. "
        f"Extracted token: '{extracted_token}'"
    )