# test_final_state.py

import os
import subprocess
import pytest

def test_black_frames_count():
    """Part 1: Verify the black frames count."""
    count_file = "/home/user/black_frames.txt"
    assert os.path.exists(count_file), f"File {count_file} does not exist."

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "7", f"Expected black frames count to be 7, but got {content}."

def test_payload_sanitizer_corpus():
    """Part 2: Verify the C program against the adversarial corpus."""
    filter_bin = "/home/user/filter"
    assert os.path.exists(filter_bin), f"Filter binary {filter_bin} does not exist."
    assert os.access(filter_bin, os.X_OK), f"Filter binary {filter_bin} is not executable."

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        result = subprocess.run([filter_bin, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([filter_bin, ef], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_failed)}")

    assert not error_messages, "Corpus verification failed:\n" + "\n".join(error_messages)

def test_automation_script():
    """Part 3: Verify the automation script behavior."""
    script_path = "/home/user/automation.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    incoming_dir = "/app/incoming/"
    safe_dir = "/home/user/safe/"

    # If the student hasn't run the script yet, incoming will have files.
    # We run the script to ensure it performs the required actions.
    if os.path.exists(incoming_dir) and os.listdir(incoming_dir):
        subprocess.run([script_path], check=False)

    assert os.path.exists(safe_dir), f"Safe directory {safe_dir} was not created."
    assert os.path.isdir(safe_dir), f"{safe_dir} is not a directory."

    incoming_files = os.listdir(incoming_dir) if os.path.exists(incoming_dir) else []
    assert len(incoming_files) == 0, f"Incoming directory is not empty. Files remaining: {', '.join(incoming_files)}"

    safe_files = os.listdir(safe_dir)
    assert len(safe_files) == 10, f"Expected exactly 10 clean files in {safe_dir}, but found {len(safe_files)}."