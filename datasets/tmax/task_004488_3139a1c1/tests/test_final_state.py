# test_final_state.py

import os
import subprocess
import pytest

def test_verifier_script_exists():
    path = "/home/user/pipeline/verifier.py"
    assert os.path.isfile(path), f"Missing required script: {path}"

def test_adversarial_corpus():
    verifier_path = "/home/user/pipeline/verifier.py"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_clean = []
    for cf in clean_files:
        result = subprocess.run(["python3", verifier_path, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        result = subprocess.run(["python3", verifier_path, ef], capture_output=True)
        # Evil files must be rejected (exit code != 0)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    assert not failed_clean and not failed_evil, " | ".join(error_messages)