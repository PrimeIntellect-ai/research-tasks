# test_final_state.py
import os
import subprocess
import pytest

def test_meta_extractor_compiles():
    """Verify that the meta-extractor code successfully compiles."""
    src_dir = "/home/user/meta-extractor"
    assert os.path.isdir(src_dir), f"{src_dir} directory is missing"

    result = subprocess.run(["go", "build"], cwd=src_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"meta-extractor failed to compile:\n{result.stderr}"

def test_detector_corpus():
    """Verify the detector correctly classifies clean and evil payloads."""
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector binary {detector_path} is missing"
    assert os.access(detector_path, os.X_OK), f"Detector binary {detector_path} is not executable"

    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.bin')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.bin')]

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    failed_clean = []
    for f in clean_files:
        res = subprocess.run([detector_path, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        res = subprocess.run([detector_path, f], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(f))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean[:5])}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil[:5])}")

    assert not error_msgs, " | ".join(error_msgs)

def test_red_frame_count():
    """Verify the red frame count is exactly 7."""
    count_file = "/home/user/red_frame_count.txt"
    assert os.path.isfile(count_file), f"{count_file} is missing"

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "7", f"Expected red frame count to be '7', but got '{content}'"