# test_final_state.py
import os
import subprocess
import pytest

def test_detector_adversarial_corpus():
    script_path = "/home/user/detector.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(clean_dir), f"Missing clean corpus dir: {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing evil corpus dir: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["/bin/bash", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["/bin/bash", script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))