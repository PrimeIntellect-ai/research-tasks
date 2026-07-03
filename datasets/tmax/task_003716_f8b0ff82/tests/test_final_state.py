# test_final_state.py

import json
import os
import pytest

def test_final_output_mse():
    """
    Validates that the final output JSON contains the correct sorted integers
    transcribed from the audio file, evaluated using Mean Squared Error.
    """
    file_path = '/home/user/final_output.json'
    assert os.path.exists(file_path), f"Expected output file not found at {file_path}"

    truth = [1, 4, 8, 16, 17, 23, 42, 55, 88, 99]

    try:
        with open(file_path, 'r') as f:
            pred = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse JSON from {file_path}: {e}")

    assert isinstance(pred, list), f"Expected the JSON file to contain a list, but got {type(pred).__name__}"
    assert len(pred) > 0, "The output JSON list is empty."

    # Pad or truncate pred to match length
    if len(pred) < len(truth):
        pred.extend([0] * (len(truth) - len(pred)))
    elif len(pred) > len(truth):
        pred = pred[:len(truth)]

    mse = sum((p - t) ** 2 for p, t in zip(pred, truth)) / len(truth)

    threshold = 5.0
    assert mse <= threshold, (
        f"MSE is too high: {mse} > {threshold}. "
        f"The predicted array was {pred}, but the truth is {truth}."
    )