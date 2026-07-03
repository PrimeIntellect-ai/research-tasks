# test_final_state.py
import subprocess
import json
import os
import pytest

CLEAN_CORPUS = "/app/corpus/clean/"
EVIL_CORPUS = "/app/corpus/evil/"
DETECTOR_SCRIPT = "/home/user/detector.py"
CLEAN_OUTPUT = "/tmp/clean_results.json"
EVIL_OUTPUT = "/tmp/evil_results.json"

def test_detector_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def test_clean_corpus_classification():
    # Run detector on clean corpus
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, "--input", CLEAN_CORPUS, "--output", CLEAN_OUTPUT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Detector script failed on clean corpus:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.isfile(CLEAN_OUTPUT), f"Output JSON not created at {CLEAN_OUTPUT}"

    with open(CLEAN_OUTPUT, 'r') as f:
        clean_results = json.load(f)

    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.wav')]
    failures = []
    for cf in clean_files:
        if cf not in clean_results:
            failures.append(f"{cf} (missing)")
        elif clean_results[cf] != "clean":
            failures.append(f"{cf} (got {clean_results[cf]})")

    assert not failures, f"{len(failures)} of {len(clean_files)} clean files modified/misclassified: {', '.join(failures)}"

def test_evil_corpus_classification():
    # Run detector on evil corpus
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, "--input", EVIL_CORPUS, "--output", EVIL_OUTPUT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Detector script failed on evil corpus:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.isfile(EVIL_OUTPUT), f"Output JSON not created at {EVIL_OUTPUT}"

    with open(EVIL_OUTPUT, 'r') as f:
        evil_results = json.load(f)

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.wav')]
    failures = []
    for ef in evil_files:
        if ef not in evil_results:
            failures.append(f"{ef} (missing)")
        elif evil_results[ef] != "corrupted":
            failures.append(f"{ef} (got {evil_results[ef]})")

    assert not failures, f"{len(failures)} of {len(evil_files)} evil files bypassed/misclassified: {', '.join(failures)}"