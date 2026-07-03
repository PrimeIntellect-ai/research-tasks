# test_final_state.py

import os
import subprocess
import pytest

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
EXECUTABLE = "/home/user/primer_filter"
SVG_FILE = "/home/user/gc_density.svg"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} not found."
    assert os.access(EXECUTABLE, os.X_OK), f"{EXECUTABLE} is not executable."

def test_svg_exists_and_not_empty():
    assert os.path.isfile(SVG_FILE), f"SVG file {SVG_FILE} not found."
    assert os.path.getsize(SVG_FILE) > 0, f"SVG file {SVG_FILE} is empty."
    with open(SVG_FILE, "r") as f:
        content = f.read()
    assert "<svg" in content.lower(), f"{SVG_FILE} does not appear to be a valid SVG file."

def test_adversarial_corpus_clean():
    if not os.path.isdir(CLEAN_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_DIR} not found.")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith(".fasta") or f.endswith(".fa")]
    if not clean_files:
        pytest.skip(f"No FASTA files found in {CLEAN_DIR}.")

    failed_clean = []
    for f in clean_files:
        result = subprocess.run([EXECUTABLE, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean files were incorrectly rejected: {', '.join(failed_clean[:10])}"

def test_adversarial_corpus_evil():
    if not os.path.isdir(EVIL_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_DIR} not found.")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith(".fasta") or f.endswith(".fa")]
    if not evil_files:
        pytest.skip(f"No FASTA files found in {EVIL_DIR}.")

    bypassed_evil = []
    for f in evil_files:
        result = subprocess.run([EXECUTABLE, f], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(os.path.basename(f))

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed the filter: {', '.join(bypassed_evil[:10])}"