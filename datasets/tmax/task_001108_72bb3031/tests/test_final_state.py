# test_final_state.py

import os
import subprocess
import cv2
import numpy as np
import pytest

def test_inference_mae():
    """
    Validates that the inference.sh script predicts the frame index with an MAE <= 20.0
    on a hidden test set of frames generated from a similar mechanical process.
    """
    # Find inference.sh
    possible_paths = ["./inference.sh", "/workspace/inference.sh", "/home/user/inference.sh"]
    inference_script = None
    for p in possible_paths:
        if os.path.isfile(p):
            inference_script = os.path.abspath(p)
            break

    assert inference_script is not None, "inference.sh not found in the expected directories."
    assert os.access(inference_script, os.X_OK), f"{inference_script} is not executable. Please ensure it has execute permissions."

    # Generate test frames
    test_dir = '/tmp/test_frames'
    os.makedirs(test_dir, exist_ok=True)
    actuals = []

    # Set a fixed seed for reproducibility of the test evaluation
    np.random.seed(42)

    for i in range(100):
        frame_idx = i * 3
        actuals.append(frame_idx)
        frame = np.zeros((128, 128), dtype=np.uint8)
        center = (int(10 + frame_idx * (108/300)), int(64 + 30 * np.sin(frame_idx / 10.0)))
        cv2.circle(frame, center, 15, 255, -1)
        noise = np.random.randint(0, 50, (128, 128), dtype=np.uint8)
        frame = cv2.add(frame, noise)
        cv2.imwrite(f'{test_dir}/frame_{i}.jpg', frame)

    # Run inference.sh on test frames
    errors = []
    for i, actual in enumerate(actuals):
        img_path = f'{test_dir}/frame_{i}.jpg'
        result = subprocess.run([inference_script, img_path], capture_output=True, text=True)

        stdout_val = result.stdout.strip()
        try:
            pred = float(stdout_val)
            errors.append(abs(pred - actual))
        except ValueError:
            # Penalty for failure to output a valid float
            errors.append(300.0)

    mae = sum(errors) / len(errors)

    assert mae <= 20.0, f"Expected MAE <= 20.0, but got {mae:.2f}. The model predictions are not accurate enough."