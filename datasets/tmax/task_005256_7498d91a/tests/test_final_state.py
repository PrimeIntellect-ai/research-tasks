# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_classifier_exists():
    script_path = "/home/user/classifier.py"
    assert os.path.exists(script_path), f"Classifier script is missing at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

def test_plot_exists():
    plot_path = "/home/user/threshold_analysis.png"
    assert os.path.exists(plot_path), f"Plot is missing at {plot_path}"
    assert os.path.isfile(plot_path), f"{plot_path} is not a file"

def test_adversarial_corpus():
    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.npy"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.npy"))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"

    clean_failures = []
    evil_failures = []

    # Test clean corpus (must exit with 0)
    for f in clean_files:
        result = subprocess.run(["python3", "/home/user/classifier.py", f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    # Test evil corpus (must exit with 1)
    for f in evil_files:
        result = subprocess.run(["python3", "/home/user/classifier.py", f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))