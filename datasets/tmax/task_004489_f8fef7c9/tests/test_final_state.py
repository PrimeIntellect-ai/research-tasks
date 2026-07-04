# test_final_state.py
import os
import glob
import subprocess
import pytest

CLEAN_DIR = "/home/user/data/clean"
EVIL_DIR = "/home/user/data/evil"
VALIDATE_SCRIPT = "/home/user/validate.py"

def test_validate_script_exists():
    assert os.path.isfile(VALIDATE_SCRIPT), f"Validation script not found at {VALIDATE_SCRIPT}"

def test_data_directories_exist():
    assert os.path.isdir(CLEAN_DIR), f"Clean data directory not found at {CLEAN_DIR}. Did you download and extract the archive?"
    assert os.path.isdir(EVIL_DIR), f"Evil data directory not found at {EVIL_DIR}. Did you download and extract the archive?"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}."
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}."

    clean_failed = []
    for cf in clean_files:
        if not os.path.isfile(cf):
            continue
        res = subprocess.run(["python3", VALIDATE_SCRIPT, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        if not os.path.isfile(ef):
            continue
        res = subprocess.run(["python3", VALIDATE_SCRIPT, ef], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)