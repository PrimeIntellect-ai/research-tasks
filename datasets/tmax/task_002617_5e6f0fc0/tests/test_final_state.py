# test_final_state.py

import os
import glob
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.py"

def test_filter_script_exists():
    assert os.path.isfile(FILTER_SCRIPT), f"The script {FILTER_SCRIPT} does not exist."

def test_adversarial_corpus_evaluation():
    assert os.path.isfile(FILTER_SCRIPT), f"Missing {FILTER_SCRIPT}"

    clean_dirs = ["/home/user/corpus/clean", "/verify/corpus/clean"]
    evil_dirs = ["/home/user/corpus/evil", "/verify/corpus/evil"]

    clean_files = []
    for d in clean_dirs:
        clean_files.extend(glob.glob(os.path.join(d, "*.bin")))

    evil_files = []
    for d in evil_dirs:
        evil_files.extend(glob.glob(os.path.join(d, "*.bin")))

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failed = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", FILTER_SCRIPT, filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            clean_failed.append(os.path.basename(filepath))

    evil_failed = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", FILTER_SCRIPT, filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 1:
            evil_failed.append(os.path.basename(filepath))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(clean_failed[:10])}" + ("..." if len(clean_failed) > 10 else ""))

    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(evil_failed[:10])}" + ("..." if len(evil_failed) > 10 else ""))

    if errors:
        pytest.fail(" | ".join(errors))