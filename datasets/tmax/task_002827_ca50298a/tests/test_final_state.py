# test_final_state.py

import os
import subprocess
import pytest

def test_engine_secret_recovered():
    secret_path = "/home/user/.engine_secret"
    assert os.path.exists(secret_path), f"Missing secret file: {secret_path}"
    with open(secret_path, "r") as f:
        content = f.read().strip()
    assert content == "a9f3b2c1", f"Incorrect secret content. Expected 'a9f3b2c1', got '{content}'"

def test_filter_script_exists():
    filter_path = "/home/user/filter.py"
    assert os.path.isfile(filter_path), f"Filter script not found at {filter_path}"

def test_adversarial_corpus_evil():
    evil_dir = "/app/corpora/evil"
    filter_path = "/home/user/filter.py"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.bin')]
    assert len(evil_files) > 0, "No evil files found in corpus"

    bypassed = []
    for fpath in evil_files:
        result = subprocess.run(
            ["python3", filter_path, fpath],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "EVIL":
            bypassed.append(os.path.basename(fpath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_adversarial_corpus_clean():
    clean_dir = "/app/corpora/clean"
    filter_path = "/home/user/filter.py"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.bin')]
    assert len(clean_files) > 0, "No clean files found in corpus"

    modified = []
    for fpath in clean_files:
        result = subprocess.run(
            ["python3", filter_path, fpath],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "CLEAN":
            modified.append(os.path.basename(fpath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(modified)}")