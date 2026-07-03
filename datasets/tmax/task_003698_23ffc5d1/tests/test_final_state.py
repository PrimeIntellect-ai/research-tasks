# test_final_state.py

import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.exists(detector_path), f"Missing file: {detector_path}"
    assert os.path.isfile(detector_path), f"Not a file: {detector_path}"
    assert os.access(detector_path, os.X_OK), f"File is not executable: {detector_path}"

def test_detector_clean_corpus():
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    subdirs = [os.path.join(clean_dir, d) for d in os.listdir(clean_dir) if os.path.isdir(os.path.join(clean_dir, d))]
    assert len(subdirs) > 0, f"No subdirectories found in {clean_dir}"

    failed_clean = []
    for subdir in subdirs:
        result = subprocess.run([detector_path, subdir], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(subdir))

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(subdirs)} clean modified/rejected. Offending: {', '.join(failed_clean)}")

def test_detector_evil_corpus():
    detector_path = "/home/user/detector"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    subdirs = [os.path.join(evil_dir, d) for d in os.listdir(evil_dir) if os.path.isdir(os.path.join(evil_dir, d))]
    assert len(subdirs) > 0, f"No subdirectories found in {evil_dir}"

    failed_evil = []
    for subdir in subdirs:
        result = subprocess.run([detector_path, subdir], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(subdir))

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(subdirs)} evil bypassed. Offending: {', '.join(failed_evil)}")