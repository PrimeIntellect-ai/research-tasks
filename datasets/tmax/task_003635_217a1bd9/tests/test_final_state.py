# test_final_state.py
import os
import subprocess
import pytest

def test_log_classifier_exists():
    script_path = "/home/user/log_classifier.py"
    assert os.path.isfile(script_path), f"Expected script not found at {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/log_classifier.py"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    total_clean = len(clean_files)
    total_evil = len(evil_files)

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {total_evil} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {total_clean} clean modified: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))