# test_final_state.py

import os
import subprocess
import pytest

EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
VALIDATE_SCRIPT = "/home/user/validate.py"

def test_validate_script_exists():
    assert os.path.isfile(VALIDATE_SCRIPT), f"The script {VALIDATE_SCRIPT} does not exist."

def test_vendored_package_fixed():
    config_file = "/app/gq_engine-1.0.4/gq_engine/config.py"
    assert os.path.isfile(config_file), f"File {config_file} does not exist."
    with open(config_file, "r") as f:
        content = f.read()
    assert "MAX_RECURSION_DEPTH = -1" not in content, "The perturbation in config.py was not fixed."

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]

    assert len(evil_files) > 0, "No evil files found."
    assert len(clean_files) > 0, "No clean files found."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["python", VALIDATE_SCRIPT, "--file", evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["python", VALIDATE_SCRIPT, "--file", clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus validation failed:\n" + "\n".join(errors)