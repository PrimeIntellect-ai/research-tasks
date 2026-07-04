# test_final_state.py
import os
import subprocess
import pytest

def test_classifier_exists():
    assert os.path.isfile("/home/user/classifier.py"), "classifier.py not found at /home/user/classifier.py"

def test_adversarial_corpus():
    script_path = "/home/user/classifier.py"
    clean_dir = "/app/simulations/clean/"
    evil_dir = "/app/simulations/evil/"

    assert os.path.isdir(clean_dir), f"Clean dir not found: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil dir not found: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.h5')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.h5')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))