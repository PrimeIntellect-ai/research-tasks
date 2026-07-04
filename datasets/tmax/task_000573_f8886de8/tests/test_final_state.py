# test_final_state.py

import os
import pytest

def test_accuracy_file():
    """Check if accuracy.txt exists and contains the correct accuracy."""
    path = "/home/user/accuracy.txt"
    assert os.path.exists(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        accuracy = float(content)
    except ValueError:
        pytest.fail(f"Could not parse accuracy as float: {content}")

    assert abs(accuracy - 0.923) < 0.01, f"Accuracy {accuracy} is not within 0.01 of expected 0.923"

def test_inference_time_file():
    """Check if inference_time.txt exists and contains a valid positive float."""
    path = "/home/user/inference_time.txt"
    assert os.path.exists(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        inference_time = float(content)
    except ValueError:
        pytest.fail(f"Could not parse inference time as float: {content}")

    assert inference_time > 0.0, f"Inference time must be strictly positive, got {inference_time}"

def test_confusion_matrix_image():
    """Check if confusion_matrix.png exists and is a valid image size."""
    path = "/home/user/confusion_matrix.png"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

    size = os.path.getsize(path)
    assert size > 5000, f"Confusion matrix image is too small ({size} bytes). It might be blank or corrupted."