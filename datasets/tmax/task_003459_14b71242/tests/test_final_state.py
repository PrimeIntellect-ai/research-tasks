# test_final_state.py
import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector script at {detector_path} is not executable"

def test_detector_clean_corpus():
    detector_path = "/home/user/detector.py"
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), "Clean corpus directory missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean files found"

    failed_files = []
    for img in clean_files:
        result = subprocess.run([detector_path, img], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(img))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_detector_evil_corpus():
    detector_path = "/home/user/detector.py"
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), "Evil corpus directory missing"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil files found"

    failed_files = []
    for img in evil_files:
        result = subprocess.run([detector_path, img], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(img))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")

def test_extracted_frames():
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Frames directory not found at {frames_dir}"

    expected_frames = [f"{i:03d}.png" for i in range(1, 11)]
    actual_frames = set(os.listdir(frames_dir))

    missing = set(expected_frames) - actual_frames
    assert not missing, f"Missing extracted frames: {sorted(missing)}"

def test_clean_frames_txt():
    txt_path = "/home/user/clean_frames.txt"
    assert os.path.isfile(txt_path), f"Clean frames list not found at {txt_path}"

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "001.png",
        "002.png",
        "004.png",
        "005.png",
        "006.png",
        "009.png",
        "010.png"
    ]

    assert lines == expected, f"Expected clean frames list to be {expected}, but got {lines}"