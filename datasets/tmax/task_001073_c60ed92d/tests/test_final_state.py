# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_sanitiser_script_exists():
    script_path = "/home/user/sanitiser.py"
    assert os.path.isfile(script_path), f"Sanitiser script is missing at {script_path}"

def test_adversarial_corpus_evaluation():
    script_path = "/home/user/sanitiser.py"
    evil_corpus_dir = "/app/corpus/evil/"
    clean_corpus_dir = "/app/corpus/clean/"

    evil_files = sorted(glob.glob(os.path.join(evil_corpus_dir, "*.json")))
    clean_files = sorted(glob.glob(os.path.join(clean_corpus_dir, "*.json")))

    assert len(evil_files) > 0, f"No JSON files found in evil corpus: {evil_corpus_dir}"
    assert len(clean_files) > 0, f"No JSON files found in clean corpus: {clean_corpus_dir}"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (must exit with 1)
    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", script_path, evil_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus (must exit with 0)
    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", script_path, clean_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail("; ".join(errors))