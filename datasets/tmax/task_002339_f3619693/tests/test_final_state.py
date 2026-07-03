# test_final_state.py

import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector binary not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector binary at {detector_path} is not executable"

def test_detector_against_corpora():
    detector_path = "/home/user/detector"
    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus_dir), f"Clean corpus dir not found: {clean_corpus_dir}"
    assert os.path.isdir(evil_corpus_dir), f"Evil corpus dir not found: {evil_corpus_dir}"

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus"
    assert len(evil_files) > 0, "No files found in evil corpus"

    clean_failed = []
    for clean_file in clean_files:
        result = subprocess.run([detector_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    evil_failed = []
    for evil_file in evil_files:
        result = subprocess.run([detector_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(evil_file))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not errors, "\n".join(errors)