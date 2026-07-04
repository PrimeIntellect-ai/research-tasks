# test_final_state.py

import os
import subprocess
import pytest

def test_detector_exists():
    detector_path = "/home/user/detector.py"
    assert os.path.exists(detector_path), f"Expected detector script at {detector_path} does not exist."
    assert os.path.isfile(detector_path), f"{detector_path} is not a file."

def test_detector_on_clean_corpus():
    detector_path = "/home/user/detector.py"
    clean_dir = "/app/hidden_corpus/clean/"

    assert os.path.exists(clean_dir), f"Clean corpus directory {clean_dir} does not exist."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.h5')]
    assert len(clean_files) > 0, f"No HDF5 files found in clean corpus {clean_dir}."

    modified = []
    for fpath in clean_files:
        result = subprocess.run(["python", detector_path, fpath], capture_output=True)
        if result.returncode != 0:
            modified.append(os.path.basename(fpath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified: {', '.join(modified)}")

def test_detector_on_evil_corpus():
    detector_path = "/home/user/detector.py"
    evil_dir = "/app/hidden_corpus/evil/"

    assert os.path.exists(evil_dir), f"Evil corpus directory {evil_dir} does not exist."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.h5')]
    assert len(evil_files) > 0, f"No HDF5 files found in evil corpus {evil_dir}."

    bypassed = []
    for fpath in evil_files:
        result = subprocess.run(["python", detector_path, fpath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(fpath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")