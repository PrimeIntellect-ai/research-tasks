# test_final_state.py
import os
import subprocess
import pytest

def test_detector_exists():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector binary {detector_path} is missing."
    assert os.access(detector_path, os.X_OK), f"Detector binary {detector_path} is not executable."

def test_evil_corpus_rejected():
    detector_path = "/home/user/detector"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, f"No files found in {evil_dir}."

    bypassed_files = []
    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        result = subprocess.run([detector_path, file_path], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(f)

    assert len(bypassed_files) == 0, f"{len(bypassed_files)} of {len(evil_files)} evil payloads bypassed the detector. Offending files: {', '.join(bypassed_files)}"

def test_clean_corpus_accepted():
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, f"No files found in {clean_dir}."

    modified_files = []
    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        result = subprocess.run([detector_path, file_path], capture_output=True)
        if result.returncode != 0:
            modified_files.append(f)

    assert len(modified_files) == 0, f"{len(modified_files)} of {len(clean_files)} clean payloads were flagged. Offending files: {', '.join(modified_files)}"