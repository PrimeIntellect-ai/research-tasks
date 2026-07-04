# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/bin/detector"
    assert os.path.isfile(detector_path), f"Detector binary not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector binary at {detector_path} is not executable"

def test_adversarial_corpus():
    detector_path = "/home/user/bin/detector"
    clean_corpus_path = "/home/user/corpus/clean"
    evil_corpus_path = "/home/user/corpus/evil"

    clean_files = sorted(glob.glob(os.path.join(clean_corpus_path, "*.json")))
    evil_files = sorted(glob.glob(os.path.join(evil_corpus_path, "*.json")))

    assert len(clean_files) > 0, f"No JSON files found in clean corpus at {clean_corpus_path}"
    assert len(evil_files) > 0, f"No JSON files found in evil corpus at {evil_corpus_path}"

    clean_failed = []
    for clean_file in clean_files:
        with open(clean_file, "r") as f:
            result = subprocess.run([detector_path], stdin=f)
            if result.returncode != 0:
                clean_failed.append(os.path.basename(clean_file))

    evil_failed = []
    for evil_file in evil_files:
        with open(evil_file, "r") as f:
            result = subprocess.run([detector_path], stdin=f)
            if result.returncode != 1:
                evil_failed.append(os.path.basename(evil_file))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (expected exit code 0, got otherwise): " + ", ".join(clean_failed))
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (expected exit code 1, got otherwise): " + ", ".join(evil_failed))

    if errors:
        pytest.fail(" | ".join(errors))

def test_log_processor_exists_and_executable():
    processor_path = "/home/user/bin/log_processor"
    assert os.path.isfile(processor_path), f"log_processor binary not found at {processor_path}"
    assert os.access(processor_path, os.X_OK), f"log_processor binary at {processor_path} is not executable"