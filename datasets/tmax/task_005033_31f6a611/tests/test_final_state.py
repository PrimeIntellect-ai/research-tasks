# test_final_state.py

import os
import subprocess
import pytest

def test_backup_count():
    count_file = "/home/user/backup_count.txt"
    assert os.path.exists(count_file), f"File {count_file} does not exist. Did you complete Part 1?"

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "7", f"Expected backup count to be '7', but got '{content}' in {count_file}"

def test_query_filter_binary_exists():
    binary_path = "/home/user/query_filter/target/release/query_filter"
    assert os.path.exists(binary_path), f"Rust binary not found at {binary_path}. Did you compile it in release mode?"
    assert os.path.isfile(binary_path), f"Expected {binary_path} to be a file."
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_adversarial_corpus_filtering():
    binary_path = "/home/user/query_filter/target/release/query_filter"
    clean_corpus_dir = "/app/hidden_corpus/clean"
    evil_corpus_dir = "/app/hidden_corpus/evil"

    assert os.path.exists(clean_corpus_dir), f"Clean corpus directory missing at {clean_corpus_dir}"
    assert os.path.exists(evil_corpus_dir), f"Evil corpus directory missing at {evil_corpus_dir}"

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus directory."
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([binary_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([binary_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(evil_failed)}")

    assert not errors, "Adversarial corpus validation failed:\n" + "\n".join(errors)