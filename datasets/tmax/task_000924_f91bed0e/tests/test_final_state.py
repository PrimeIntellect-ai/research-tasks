# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_reference_frame_extracted():
    frame_path = "/home/user/reference_frame.raw"
    assert os.path.exists(frame_path), f"Missing reference_frame.raw at {frame_path}"
    assert os.path.isfile(frame_path), f"Not a file: {frame_path}"

    size = os.path.getsize(frame_path)
    expected_size = 640 * 480  # 307200 bytes
    assert size == expected_size, f"Invalid frame size: expected {expected_size}, got {size}. Ensure it is 8-bit grayscale at 640x480."

def test_sanitizer_executable_exists():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.exists(sanitizer_path), f"Missing sanitizer executable at {sanitizer_path}"
    assert os.path.isfile(sanitizer_path), f"Not a file: {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer is not executable: {sanitizer_path}"

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.dat"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([sanitizer_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitizer"
    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.dat"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    bypassed_files = []
    for f in evil_files:
        result = subprocess.run([sanitizer_path, f], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(f))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(bypassed_files)}")