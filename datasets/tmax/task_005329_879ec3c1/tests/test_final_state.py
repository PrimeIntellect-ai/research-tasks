# test_final_state.py
import os
import subprocess
import pytest

def test_classifier_exists():
    binary_path = "/home/user/log_classifier"
    assert os.path.isfile(binary_path), f"The classifier binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The classifier binary {binary_path} is not executable."

def test_classifier_accuracy():
    binary_path = "/home/user/log_classifier"
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus missing at {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    for ef in evil_files:
        result = subprocess.run([binary_path, ef], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            evil_bypassed.append(os.path.basename(ef))

    for cf in clean_files:
        result = subprocess.run([binary_path, cf], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            clean_modified.append(os.path.basename(cf))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_task_complete_log_exists():
    log_path = "/home/user/task_complete.log"
    assert os.path.isfile(log_path), f"The file {log_path} is missing."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "CLASSIFIER READY" in content, f"Expected 'CLASSIFIER READY' in {log_path}"