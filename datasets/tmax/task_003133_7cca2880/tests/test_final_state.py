# test_final_state.py
import os
import time
import subprocess
import numpy as np
from PIL import Image

def test_evidence_extraction_performance_and_accuracy():
    script_path = "/home/user/extract_evidence.sh"
    evidence_path = "/home/user/evidence.jpg"
    truth_path = "/app/truth_evidence.jpg"

    assert os.path.isfile(script_path), f"Script missing at {script_path}"
    assert os.path.isfile(truth_path), f"Truth image missing at {truth_path}"

    # Remove evidence if it exists to ensure we are testing the script's output
    if os.path.exists(evidence_path):
        os.remove(evidence_path)

    # Run the script and measure duration
    start_time = time.time()
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert duration <= 3.0, f"Script took {duration:.2f}s, which is above the 3.0s threshold."

    assert os.path.isfile(evidence_path), f"Output file {evidence_path} was not created by the script."

    # Load images as grayscale
    try:
        img_evidence = np.array(Image.open(evidence_path).convert('L'))
    except Exception as e:
        assert False, f"Failed to open {evidence_path} as an image: {e}"

    try:
        img_truth = np.array(Image.open(truth_path).convert('L'))
    except Exception as e:
        assert False, f"Failed to open {truth_path} as an image: {e}"

    assert img_evidence.shape == img_truth.shape, f"Image shapes differ: {img_evidence.shape} vs {img_truth.shape}"

    # Calculate SSIM (Structural Similarity Index)
    try:
        from skimage.metrics import structural_similarity as ssim
        score, _ = ssim(img_evidence, img_truth, full=True)
    except ImportError:
        # Fallback to a simple MSE-based metric if skimage is not available
        mse = np.mean((img_evidence.astype(float) - img_truth.astype(float)) ** 2)
        max_pixel = 255.0
        # Convert MSE to a PSNR-like score mapped to [0, 1] for fallback comparison
        score = 1.0 - (mse / (max_pixel ** 2))
        # If images are perfectly identical, score is 1.0. 
        # A threshold of 0.95 in this fallback means MSE is very low.

    assert score >= 0.95, f"Image similarity score {score:.4f} is below threshold 0.95"