# test_final_state.py

import os
import subprocess
import pytest

def test_extracted_seed():
    seed_file = "/home/user/extracted_seed.txt"
    assert os.path.exists(seed_file), f"Seed file missing: {seed_file}"

    with open(seed_file, "r") as f:
        content = f.read()

    assert "8x9F2a_poly" in content, f"Extracted seed is incorrect. Found: {content.strip()}"

def test_filter_script_exists():
    script_path = "/home/user/filter.py"
    assert os.path.exists(script_path), f"Filter script missing: {script_path}"
    assert os.path.isfile(script_path), f"Filter script is not a file: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/filter.py"
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.exists(script_path), f"Script not found at {script_path}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_rejected = []

    for fpath in evil_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    for fpath in clean_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(fpath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed}")
    if clean_rejected:
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {clean_rejected}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))