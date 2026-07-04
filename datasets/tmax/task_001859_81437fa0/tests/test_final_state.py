# test_final_state.py
import os
import subprocess
import pytest

def test_detector_script_exists():
    script_path = "/home/user/detector.py"
    assert os.path.exists(script_path), f"Detector script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_adversarial_corpus():
    script_path = "/home/user/detector.py"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(clean_dir), f"Clean directory {clean_dir} missing."
    assert os.path.exists(evil_dir), f"Evil directory {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, f"No files found in {clean_dir}"
    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    bypassed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(evil_file))

    flagged_clean = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            flagged_clean.append(os.path.basename(clean_file))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if flagged_clean:
        error_msgs.append(f"{len(flagged_clean)} of {len(clean_files)} clean modified/flagged: {', '.join(flagged_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))