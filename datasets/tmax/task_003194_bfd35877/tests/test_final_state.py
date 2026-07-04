# test_final_state.py

import os
import subprocess
import pytest

def test_query_filter_executable():
    executable_path = "/home/user/query_filter"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_adversarial_corpus():
    executable_path = "/home/user/query_filter"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        file_path = os.path.join(clean_dir, cf)
        with open(file_path, 'r') as f:
            result = subprocess.run([executable_path], stdin=f, capture_output=True, text=True)

        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            clean_failed.append(cf)

    evil_bypassed = []
    for ef in evil_files:
        file_path = os.path.join(evil_dir, ef)
        with open(file_path, 'r') as f:
            result = subprocess.run([executable_path], stdin=f, capture_output=True, text=True)

        output = result.stdout.strip()
        if result.returncode != 1 or output != "EVIL":
            evil_bypassed.append(ef)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))