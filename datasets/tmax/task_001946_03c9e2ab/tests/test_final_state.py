# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_exists():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Missing detector script at {detector_path}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector.py"
    clean_dir = "/eval/data/clean"
    evil_dir = "/eval/data/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.h5"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.h5"))

    assert len(clean_files) > 0, f"No clean evaluation files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil evaluation files found in {evil_dir}"

    failed_clean = []
    for f in clean_files:
        res = subprocess.run(["python3", detector_path, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        res = subprocess.run(["python3", detector_path, f], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(f))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (rejected/failed): {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed (accepted): {', '.join(failed_evil)}")

    if errors:
        pytest.fail(" | ".join(errors))