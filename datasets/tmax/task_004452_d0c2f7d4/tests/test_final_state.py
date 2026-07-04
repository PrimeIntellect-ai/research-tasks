# test_final_state.py
import os
import subprocess
import pytest

def test_executable_exists():
    executable = "/app/build/config_filter"
    assert os.path.isfile(executable), f"Executable {executable} not found. Did you build it?"
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_adversarial_corpus():
    executable = "/app/build/config_filter"
    clean_dir = "/app/hidden_clean"
    evil_dir = "/app/hidden_evil"

    assert os.path.isdir(clean_dir), f"Directory {clean_dir} missing"
    assert os.path.isdir(evil_dir), f"Directory {evil_dir} missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed_clean = []
    failed_evil = []

    for cf in clean_files:
        res = subprocess.run([executable, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run([executable, ef], capture_output=True)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified: {', '.join(failed_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))