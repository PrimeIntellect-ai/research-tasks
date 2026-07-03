# test_final_state.py

import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"
MODEL_RESULTS_PATH = os.path.join(WORKSPACE_DIR, "model_results.json")
PREDICTIONS_IMAGE_PATH = os.path.join(WORKSPACE_DIR, "predictions.png")

def test_model_results_exist_and_correct():
    assert os.path.isfile(MODEL_RESULTS_PATH), f"File {MODEL_RESULTS_PATH} does not exist. The script might not have run successfully."

    with open(MODEL_RESULTS_PATH, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {MODEL_RESULTS_PATH} is not valid JSON.")

    expected_keys = {"pressure_coef", "humidity_coef", "intercept"}
    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected keys. Found: {list(results.keys())}"

    # Check values with a small tolerance due to float representation, or exact string match if saved as numbers
    assert abs(results["pressure_coef"] - (-0.3204)) < 1e-4, f"Expected pressure_coef to be -0.3204, got {results['pressure_coef']}"
    assert abs(results["humidity_coef"] - 0.8177) < 1e-4, f"Expected humidity_coef to be 0.8177, got {results['humidity_coef']}"
    assert abs(results["intercept"] - 307.2144) < 1e-4, f"Expected intercept to be 307.2144, got {results['intercept']}"

def test_predictions_image_exists_and_valid():
    assert os.path.isfile(PREDICTIONS_IMAGE_PATH), f"File {PREDICTIONS_IMAGE_PATH} does not exist. The plot was not saved."

    # Check if it's a valid PNG file by reading the magic number
    with open(PREDICTIONS_IMAGE_PATH, "rb") as f:
        header = f.read(8)

    png_signature = b'\x89PNG\r\n\x1a\n'
    assert header == png_signature, f"File {PREDICTIONS_IMAGE_PATH} is not a valid PNG image."

    # Also check file size to ensure it's not just an empty file or a tiny broken file
    assert os.path.getsize(PREDICTIONS_IMAGE_PATH) > 100, f"File {PREDICTIONS_IMAGE_PATH} is too small to be a valid plot."