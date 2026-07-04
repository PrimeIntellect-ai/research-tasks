# test_final_state.py

import os
import glob
import subprocess
import json
import pytest

def test_adversarial_corpus_sanitize():
    script_path = "/home/user/sanitize.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True, text=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))
            continue

        # Verify stdout contains the JSON
        with open(cf, 'r') as f:
            expected_content = f.read().strip()

        # We check if the expected JSON is in stdout (or matches after parsing if it was reformatted, but instructions say "print the raw JSON contents")
        if expected_content not in result.stdout.strip():
            # Try parsing both to handle formatting differences
            try:
                expected_json = json.loads(expected_content)
                actual_json = json.loads(result.stdout.strip())
                if expected_json != actual_json:
                    clean_failed.append(os.path.basename(cf))
            except json.JSONDecodeError:
                clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True, text=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not error_messages, " | ".join(error_messages)

def test_led_flashes_count():
    output_file = "/home/user/led_flashes.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content == "7", f"Expected led_flashes.txt to contain '7', but got '{content}'."