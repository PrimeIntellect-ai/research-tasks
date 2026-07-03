# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_script_exists():
    script_path = "/home/user/validate_sshd.py"
    assert os.path.isfile(script_path), f"The required script {script_path} does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/validate_sshd.py"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_rejected = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_rejected.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)