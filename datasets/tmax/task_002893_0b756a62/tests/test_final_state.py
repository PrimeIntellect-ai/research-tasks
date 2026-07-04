# test_final_state.py

import os
import subprocess
import pytest

def test_phase1_extraction():
    logs_dir = "/home/user/logs"
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} does not exist. Extraction failed or was not performed."
    extracted_files = os.listdir(logs_dir)
    assert len(extracted_files) > 0, f"Directory {logs_dir} is empty. No files were extracted."

def test_phase2_filter_script():
    script_path = "/home/user/filter_records.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Ensure script is executable or can be run with bash
    # We will run it explicitly with bash to be safe, but it should ideally be executable.

    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]

    clean_failures = []
    for cf in clean_files:
        with open(cf, 'rb') as f:
            expected_output = f.read()

        result = subprocess.run(["bash", script_path, cf], capture_output=True)
        if result.stdout != expected_output:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["bash", script_path, ef], capture_output=True)
        if result.stdout != b"":
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    assert not error_messages, " | ".join(error_messages)