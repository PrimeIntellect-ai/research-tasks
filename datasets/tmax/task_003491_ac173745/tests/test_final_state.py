# test_final_state.py
import os
import json
import pytest
from PIL import Image

def test_waveform_png_exists_and_valid():
    """Verify that the waveform.png image is generated and is a valid image."""
    img_path = "/home/user/waveform.png"
    assert os.path.exists(img_path), f"{img_path} does not exist. Did you fix and run visualize.py?"

    try:
        with Image.open(img_path) as img:
            img.verify()
    except Exception as e:
        pytest.fail(f"Failed to open {img_path} as a valid image. The script might still be broken: {e}")

def test_pipeline_script_exists():
    """Verify that the pipeline.py script was created."""
    script_path = "/home/user/pipeline.py"
    assert os.path.exists(script_path), f"{script_path} does not exist."

def test_metrics_json_and_mse_threshold():
    """Verify that metrics.json exists, contains test_mse, and meets the performance threshold."""
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), f"{metrics_path} does not exist. Did you run the pipeline script?"

    with open(metrics_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {metrics_path} as JSON.")

    assert "test_mse" in data, "The key 'test_mse' was not found in metrics.json."

    test_mse = data["test_mse"]
    assert isinstance(test_mse, (int, float)), f"'test_mse' should be a number, but got {type(test_mse).__name__}."

    threshold = 1.5
    assert test_mse <= threshold, f"Fail: MSE too high. Measured test_mse is {test_mse}, which exceeds the threshold of {threshold}."