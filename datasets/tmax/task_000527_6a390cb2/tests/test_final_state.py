# test_final_state.py

import os
import subprocess
import pytest

def test_seq_filter_executable():
    executable = "/home/user/seq_filter"
    assert os.path.isfile(executable), f"Executable not found at {executable}"
    assert os.access(executable, os.X_OK), f"File at {executable} is not executable"

def test_adversarial_corpus():
    executable = "/home/user/seq_filter"
    clean_dir = "/app/eval_reads/clean"
    evil_dir = "/app/eval_reads/artifact"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.txt')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.txt')]

    assert len(clean_files) > 0, "No clean files found in evaluation directory"
    assert len(evil_files) > 0, "No evil files found in evaluation directory"

    clean_failures = []
    evil_failures = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r') as f:
            sequence = f.read().strip()

        try:
            result = subprocess.run([executable, sequence], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_failures.append(filename)
        except Exception as e:
            clean_failures.append(f"{filename} (Error: {str(e)})")

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r') as f:
            sequence = f.read().strip()

        try:
            result = subprocess.run([executable, sequence], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_failures.append(filename)
        except Exception as e:
            evil_failures.append(f"{filename} (Error: {str(e)})")

    error_msg = []
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failures[:10]) + ("..." if len(evil_failures) > 10 else ""))
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): " + ", ".join(clean_failures[:10]) + ("..." if len(clean_failures) > 10 else ""))

    assert not evil_failures and not clean_failures, " | ".join(error_msg)