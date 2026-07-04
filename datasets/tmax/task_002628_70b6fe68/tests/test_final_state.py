# test_final_state.py

import os
import subprocess
import pytest

def test_adversarial_corpus():
    script_path = "/home/user/policy_check.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    evil_bypassed = []

    for cf in clean_files:
        result = subprocess.run(["bash", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run(["bash", script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: {', '.join(clean_failed)}")

    assert not errors, " | ".join(errors)