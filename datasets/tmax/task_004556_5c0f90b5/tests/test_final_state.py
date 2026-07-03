# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists():
    script_path = "/home/user/detector.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

def test_detector_adversarial_corpus():
    script_path = "/home/user/detector.py"
    evil_dir = "/app/corpora/test/evil/"
    clean_dir = "/app/corpora/test/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_bypassed.append(os.path.basename(filepath))

    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_modified.append(os.path.basename(filepath))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:5])}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msg)

def test_video_clean_frames_txt():
    txt_path = "/home/user/video_clean_frames.txt"
    assert os.path.isfile(txt_path), f"Clean frames file not found at {txt_path}"

    with open(txt_path, "r") as f:
        lines = f.read().strip().splitlines()

    extracted_frames = []
    for line in lines:
        try:
            extracted_frames.append(int(line.strip()))
        except ValueError:
            pytest.fail(f"Invalid non-integer line in {txt_path}: {line}")

    expected_frames = [i for i in range(60) if i not in (14, 27, 42, 51)]

    assert extracted_frames == expected_frames, f"Extracted frames do not match expected. Found {len(extracted_frames)} frames, expected {len(expected_frames)}."

def test_clean_dataset_h5():
    h5_path = "/home/user/clean_dataset.h5"
    assert os.path.isfile(h5_path), f"HDF5 dataset not found at {h5_path}"

    try:
        import h5py
    except ImportError:
        pytest.fail("h5py is not installed, cannot verify HDF5 file.")

    with h5py.File(h5_path, "r") as f:
        assert "images" in f, "Dataset 'images' not found in HDF5 file."
        dataset = f["images"]

        expected_shape = (56, 720, 1280, 3)
        assert dataset.shape == expected_shape, f"Dataset shape {dataset.shape} does not match expected {expected_shape}."

        assert dataset.dtype == "uint8", f"Dataset dtype {dataset.dtype} does not match expected uint8."