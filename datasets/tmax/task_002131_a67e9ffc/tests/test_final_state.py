# test_final_state.py

import os
import subprocess
import pytest

def test_evaluate_sim_script_exists():
    script_path = "/home/user/evaluate_sim.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/evaluate_sim.py"
    evil_corpus_path = "/app/data/eval_evil/"
    clean_corpus_path = "/app/data/eval_clean/"

    assert os.path.isdir(evil_corpus_path), f"Evil corpus path {evil_corpus_path} not found."
    assert os.path.isdir(clean_corpus_path), f"Clean corpus path {clean_corpus_path} not found."

    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if f.endswith('.csv')]
    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if f.endswith('.csv')]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", script_path, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))