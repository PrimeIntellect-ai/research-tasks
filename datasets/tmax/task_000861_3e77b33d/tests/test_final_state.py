# test_final_state.py
import os
import subprocess
import pytest

def test_filter_script_exists():
    script_path = "/home/user/filter.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_adversarial_corpus_evaluation():
    script_path = "/home/user/filter.py"
    clean_dir = "/app/data/clean"
    evil_dir = "/app/data/evil"

    assert os.path.exists(clean_dir), f"Clean directory {clean_dir} is missing."
    assert os.path.exists(evil_dir), f"Evil directory {evil_dir} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for fpath in clean_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(fpath))

    evil_failures = []
    for fpath in evil_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(fpath))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected (expected exit 0). Offending files: {', '.join(clean_failures[:10])}{'...' if len(clean_failures) > 10 else ''}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (expected exit 1). Offending files: {', '.join(evil_failures[:10])}{'...' if len(evil_failures) > 10 else ''}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))