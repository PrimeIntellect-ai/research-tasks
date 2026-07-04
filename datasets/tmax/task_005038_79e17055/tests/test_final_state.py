# test_final_state.py

import os
import subprocess
import pytest

def test_red_frame_count_file():
    count_file = "/home/user/red_frame_count.txt"
    assert os.path.isfile(count_file), f"Expected file {count_file} does not exist."

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "45", f"Expected red frame count to be '45', but got '{content}'."

def test_detector_executable():
    exe_path = "/home/user/detector"
    assert os.path.isfile(exe_path), f"Executable missing at {exe_path}."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_adversarial_corpus_evaluation():
    exe_path = "/home/user/detector"
    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".csv")]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".csv")]

    assert len(evil_files) > 0, "No CSV files found in evil corpus."
    assert len(clean_files) > 0, "No CSV files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        full_path = os.path.join(evil_dir, f)
        try:
            result = subprocess.run([exe_path, full_path], capture_output=True, text=True, timeout=5)
            if result.stdout.strip() != "REJECT":
                evil_bypassed.append(f)
        except Exception:
            evil_bypassed.append(f)

    for f in clean_files:
        full_path = os.path.join(clean_dir, f)
        try:
            result = subprocess.run([exe_path, full_path], capture_output=True, text=True, timeout=5)
            if result.stdout.strip() != "ACCEPT":
                clean_modified.append(f)
        except Exception:
            clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))