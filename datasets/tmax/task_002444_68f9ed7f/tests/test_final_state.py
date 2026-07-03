# test_final_state.py
import os
import subprocess
import pytest

def test_task1_frame_avg():
    """
    Validates that the student extracted the frame at exactly 00:00:02,
    converted it to grayscale, and calculated the correct mean pixel intensity.
    """
    student_file = "/home/user/frame_avg.txt"
    assert os.path.exists(student_file), f"Student file {student_file} does not exist."

    # Compute truth
    truth_frame = "/tmp/truth_frame.png"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:02", "-i", "/app/training_source.mp4",
            "-vframes", "1", "-pix_fmt", "gray", truth_frame
        ], capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract truth frame using ffmpeg: {e.stderr.decode()}")

    # Calculate mean using numpy and PIL (available in standard ML environments)
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        pytest.fail("numpy or PIL not available to compute truth.")

    truth_val = np.mean(np.array(Image.open(truth_frame)))
    truth_str = f"{truth_val:.2f}"

    with open(student_file, "r") as f:
        student_val = f.read().strip()

    assert student_val == truth_str, f"Mean pixel intensity mismatch. Expected {truth_str}, got {student_val}"

def test_task2_filter_corpus():
    """
    Validates that the student's script correctly accepts clean files (exit code 0)
    and rejects evil files (exit code 1).
    """
    script_path = "/home/user/filter_corpus.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(clean_dir), f"Clean corpus directory {clean_dir} missing."
    assert os.path.exists(evil_dir), f"Evil corpus directory {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        res = subprocess.run([script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run([script_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_failed)}")

    assert not errors, " | ".join(errors)