# test_final_state.py

import os
import json
import subprocess
import pytest

EVIL_CORPUS_PATH = "/app/corpus/evil/"
CLEAN_CORPUS_PATH = "/app/corpus/clean/"
DETECTOR_SCRIPT = "/home/user/analysis/detector.py"
VERDICT_JSON = "/home/user/analysis/verdict.json"

def run_detector(corpus_path):
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

    # Remove previous verdict.json if it exists to ensure we are reading the fresh output
    if os.path.exists(VERDICT_JSON):
        os.remove(VERDICT_JSON)

    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, corpus_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Detector script failed on {corpus_path}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.exists(VERDICT_JSON), f"Detector script did not produce {VERDICT_JSON} for {corpus_path}"

    with open(VERDICT_JSON, 'r') as f:
        try:
            verdict = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {VERDICT_JSON} as JSON")

    return verdict

def test_evil_corpus():
    verdict = run_detector(EVIL_CORPUS_PATH)

    evil_files = [f for f in os.listdir(EVIL_CORPUS_PATH) if f.endswith('.dat')]
    assert len(evil_files) > 0, f"No .dat files found in {EVIL_CORPUS_PATH}"

    bypassed_files = []
    for f in evil_files:
        if verdict.get(f) != "evil":
            bypassed_files.append(f)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus():
    verdict = run_detector(CLEAN_CORPUS_PATH)

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_PATH) if f.endswith('.dat')]
    assert len(clean_files) > 0, f"No .dat files found in {CLEAN_CORPUS_PATH}"

    modified_files = []
    for f in clean_files:
        if verdict.get(f) != "clean":
            modified_files.append(f)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified (incorrectly classified). Offending files: {', '.join(modified_files)}")