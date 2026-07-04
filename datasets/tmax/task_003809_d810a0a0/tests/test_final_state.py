# test_final_state.py
import os
import subprocess
import pytest

def test_exploit_frame_extraction():
    frame_file = "/home/user/exploit_frame.txt"
    assert os.path.exists(frame_file), f"Expected output file missing at {frame_file}"

    with open(frame_file, "r") as f:
        content = f.read().strip()

    try:
        frame_num = int(content)
    except ValueError:
        pytest.fail(f"Content of {frame_file} is not a valid integer: '{content}'")

    assert 140 <= frame_num <= 144, f"Frame number {frame_num} is outside the acceptable range (140-144). Expected ~142."

def test_detector_adversarial_corpus():
    detector_script = "/home/user/detector.py"
    assert os.path.exists(detector_script), f"Detector script missing at {detector_script}"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.exists(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.exists(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert evil_files, "No evil files found to test against."
    assert clean_files, "No clean files found to test against."

    evil_bypassed = []
    for fpath in evil_files:
        result = subprocess.run(["python3", detector_script, fpath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    clean_modified = []
    for fpath in clean_files:
        result = subprocess.run(["python3", detector_script, fpath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(fpath))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (false positives): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))