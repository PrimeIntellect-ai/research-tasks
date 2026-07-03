# test_final_state.py
import os
import subprocess
import pytest

def test_detector_binary_exists():
    binary_path = '/home/user/detector'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_detector_on_corpora():
    binary_path = '/home/user/detector'
    clean_dir = '/app/corpora/clean'
    evil_dir = '/app/corpora/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for cf in clean_files:
        try:
            result = subprocess.run([binary_path, cf], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failures.append(os.path.basename(cf))
        except Exception as e:
            clean_failures.append(f"{os.path.basename(cf)} (error: {e})")

    evil_failures = []
    for ef in evil_files:
        try:
            result = subprocess.run([binary_path, ef], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failures.append(os.path.basename(ef))
        except Exception as e:
            evil_failures.append(f"{os.path.basename(ef)} (error: {e})")

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean files misclassified or failed: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed or failed: {', '.join(evil_failures)}")

    assert not error_msg, " | ".join(error_msg)