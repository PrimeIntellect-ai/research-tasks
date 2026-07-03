# test_final_state.py

import os
import subprocess
import pytest

def test_filter_backup_executable_exists():
    executable = "/home/user/filter_backup"
    assert os.path.isfile(executable), f"Executable not found at {executable}"
    assert os.access(executable, os.X_OK), f"File at {executable} is not executable"

def test_adversarial_corpus():
    executable = "/home/user/filter_backup"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.jsonl')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.jsonl')]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failed = []
    evil_failed = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run([executable, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "ACCEPT":
            clean_failed.append((filename, result.returncode, output))

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run([executable, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "REJECT":
            evil_failed.append((filename, result.returncode, output))

    error_messages = []
    if evil_failed:
        basenames = [f[0] for f in evil_failed]
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(basenames)}")
    if clean_failed:
        basenames = [f[0] for f in clean_failed]
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(basenames)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))