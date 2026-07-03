# test_final_state.py

import os
import time
import subprocess
import numpy as np
import pandas as pd
import pytest

def compute_ground_truth(video_path):
    import cv2
    cap = cv2.VideoCapture(video_path)
    results = []
    frame_id = 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = img.astype(float) / 255.0

        A = img[:100, :100]
        y = img[:100, 100:200].mean(axis=1)

        # Stable SVD pseudo-inverse
        if np.all(A == 0):
            x = np.zeros(A.shape[1])
        else:
            x = np.linalg.pinv(A.T @ A) @ A.T @ y

        peak_wave = np.argmax(x)
        max_int = np.max(x)

        results.append({
            'FrameID': frame_id,
            'PeakWavelength': peak_wave,
            'MaxIntensity': max_int
        })
        frame_id += 1
    cap.release()
    return pd.DataFrame(results)

def test_optimized_pipeline_performance_and_correctness():
    script_path = "/home/user/run_optimized.sh"
    assert os.path.exists(script_path), f"Missing optimized script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    video_path = "/app/spectrometer_feed.mp4"
    assert os.path.exists(video_path), f"Missing video file: {video_path}"

    output_csv = "/home/user/final_spectra.csv"
    if os.path.exists(output_csv):
        os.remove(output_csv)

    start_time = time.time()
    result = subprocess.run([script_path], capture_output=True, text=True)
    elapsed_time = time.time() - start_time

    assert result.returncode == 0, f"Optimized script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.exists(output_csv), f"Output CSV not found at {output_csv}"

    # Performance check
    baseline_time = 45.0
    speedup = baseline_time / elapsed_time
    assert speedup >= 3.0, f"Performance failed: Speedup is {speedup:.2f}x (Threshold >= 3.0x). Elapsed time: {elapsed_time:.2f}s"

    # Correctness check
    df_pred = pd.read_csv(output_csv).sort_values('FrameID').reset_index(drop=True)
    df_true = compute_ground_truth(video_path).sort_values('FrameID').reset_index(drop=True)

    assert len(df_pred) == len(df_true), f"Frame count mismatch: expected {len(df_true)}, got {len(df_pred)}"

    mse = ((df_pred['MaxIntensity'] - df_true['MaxIntensity'])**2).mean()
    assert mse < 0.001, f"Correctness failed: MSE is {mse:.6f} (Threshold < 0.001)"