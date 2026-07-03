# test_final_state.py

import os
import json
import subprocess
import pytest

EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
DETECTOR_SCRIPT = "/home/user/detector.py"
RESULTS_FILE = "/home/user/results.json"
RUST_SO_PATH = "/home/user/rust_waf/target/release/librust_waf.so"

def test_rust_library_compiled():
    assert os.path.isfile(RUST_SO_PATH), f"Rust shared library not found at {RUST_SO_PATH}. Did you successfully run cargo build --release?"

def test_detector_script_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def test_adversarial_corpus_evil():
    # Run detector on evil corpus
    result = subprocess.run(["python3", DETECTOR_SCRIPT, EVIL_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"detector.py failed on evil corpus:\n{result.stderr}"

    assert os.path.isfile(RESULTS_FILE), f"Results file not created at {RESULTS_FILE}"

    with open(RESULTS_FILE, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    bypassed = []
    for filepath in evil_files:
        if filepath not in results:
            bypassed.append(os.path.basename(filepath) + " (missing)")
        elif results[filepath] != "EVIL":
            bypassed.append(os.path.basename(filepath) + f" (scored as {results[filepath]})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_adversarial_corpus_clean():
    # Run detector on clean corpus
    result = subprocess.run(["python3", DETECTOR_SCRIPT, CLEAN_CORPUS_DIR], capture_output=True, text=True)
    assert result.returncode == 0, f"detector.py failed on clean corpus:\n{result.stderr}"

    assert os.path.isfile(RESULTS_FILE), f"Results file not created at {RESULTS_FILE}"

    with open(RESULTS_FILE, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    modified = []
    for filepath in clean_files:
        if filepath not in results:
            modified.append(os.path.basename(filepath) + " (missing)")
        elif results[filepath] != "CLEAN":
            modified.append(os.path.basename(filepath) + f" (scored as {results[filepath]})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (flagged as EVIL): {', '.join(modified)}")