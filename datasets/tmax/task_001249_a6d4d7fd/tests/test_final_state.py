# test_final_state.py
import os
import numpy as np
from PIL import Image

def test_required_files_exist():
    """Test that the student created the required files."""
    required_files = [
        "/app/clib/libfilter.so",
        "/app/proto/service.proto",
        "/app/server/main.go",
        "/app/client/main.go",
        "/app/output.png"
    ]
    for p in required_files:
        assert os.path.exists(p), f"Missing required file: {p}"

def test_output_mse():
    """
    Test the accuracy of the student's output image against the ground truth.
    The threshold for Mean Squared Error (MSE) is <= 2.0.
    """
    output_path = "/app/output.png"
    truth_path = "/tmp/truth_output.png"

    assert os.path.exists(output_path), f"Output file missing: {output_path}"
    assert os.path.exists(truth_path), f"Truth file missing: {truth_path}"

    try:
        agent_img = np.array(Image.open(output_path).convert('L'), dtype=np.float32)
    except Exception as e:
        raise AssertionError(f"Failed to read {output_path}: {e}")

    try:
        truth_img = np.array(Image.open(truth_path).convert('L'), dtype=np.float32)
    except Exception as e:
        raise AssertionError(f"Failed to read {truth_path}: {e}")

    if agent_img.shape != truth_img.shape:
        raise AssertionError(f"Output image shape mismatch: {agent_img.shape} vs expected {truth_img.shape}")

    mse = float(np.mean((agent_img - truth_img) ** 2))
    assert mse <= 2.0, f"MSE {mse:.4f} exceeds threshold 2.0. The convolution implementation or extracted kernel is incorrect."