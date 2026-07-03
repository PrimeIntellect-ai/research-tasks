# test_final_state.py

import os
import subprocess
import pytest

def test_detector_script_exists():
    detector_script = "/home/user/detector.py"
    assert os.path.exists(detector_script), f"Detector script not found at {detector_script}"
    assert os.path.isfile(detector_script), f"Detector path is not a file: {detector_script}"

def test_detector_evil_corpus():
    detector_script = "/home/user/detector.py"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(evil_dir), f"Evil corpus directory not found: {evil_dir}"

    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])
    assert len(evil_files) > 0, "Evil corpus directory is empty"

    bypassed = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(["python3", detector_script, filepath], capture_output=True, text=True)

        # Must exit with code 1 and print EVIL
        if result.returncode != 1 or "EVIL" not in result.stdout:
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_detector_clean_corpus():
    detector_script = "/home/user/detector.py"
    clean_dir = "/app/corpus/clean"

    assert os.path.exists(clean_dir), f"Clean corpus directory not found: {clean_dir}"

    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])
    assert len(clean_files) > 0, "Clean corpus directory is empty"

    modified = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(["python3", detector_script, filepath], capture_output=True, text=True)

        # Must exit with code 0 and print CLEAN
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified: {', '.join(modified)}")