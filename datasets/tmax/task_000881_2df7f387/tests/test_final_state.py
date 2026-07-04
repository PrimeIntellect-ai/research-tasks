# test_final_state.py
import os
import subprocess
from pathlib import Path

def test_filter_exists_and_executable():
    filter_path = Path("/home/user/filter")
    assert filter_path.exists(), f"Filter binary not found at {filter_path}"
    assert filter_path.is_file(), f"{filter_path} is not a file"
    assert os.access(filter_path, os.X_OK), f"Filter binary at {filter_path} is not executable"

def test_filter_against_adversarial_corpus():
    filter_path = "/home/user/filter"
    clean_corpus_dir = Path("/app/corpus/clean")
    evil_corpus_dir = Path("/app/corpus/evil")

    assert clean_corpus_dir.exists() and clean_corpus_dir.is_dir(), f"Clean corpus dir missing: {clean_corpus_dir}"
    assert evil_corpus_dir.exists() and evil_corpus_dir.is_dir(), f"Evil corpus dir missing: {evil_corpus_dir}"

    clean_files = list(clean_corpus_dir.iterdir())
    evil_files = list(evil_corpus_dir.iterdir())

    assert len(clean_files) > 0, "No files found in clean corpus"
    assert len(evil_files) > 0, "No files found in evil corpus"

    clean_failed = []
    evil_failed = []

    # Test clean corpus (expected exit code 0)
    for f in clean_files:
        if not f.is_file():
            continue
        with open(f, "rb") as stdin_file:
            result = subprocess.run([filter_path], stdin=stdin_file, capture_output=True)
            if result.returncode != 0:
                clean_failed.append(f.name)

    # Test evil corpus (expected exit code 1)
    for f in evil_files:
        if not f.is_file():
            continue
        with open(f, "rb") as stdin_file:
            result = subprocess.run([filter_path], stdin=stdin_file, capture_output=True)
            if result.returncode != 1:
                evil_failed.append(f.name)

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/blocked: {', '.join(clean_failed)}")

    if error_messages:
        assert False, " | ".join(error_messages)