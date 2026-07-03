# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/scan_patches.py"
VIDEO_PATH = "/app/salt_video.mp4"
CLEAN_CORPUS = "/app/corpus/clean/"
EVIL_CORPUS = "/app/corpus/evil/"
CLEAN_OUT = "/tmp/clean_results.json"
EVIL_OUT = "/tmp/evil_results.json"

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    # Run on clean corpus
    res_clean = subprocess.run(
        ["python3", SCRIPT_PATH, "--corpus", CLEAN_CORPUS, "--video", VIDEO_PATH, "--out", CLEAN_OUT],
        capture_output=True, text=True
    )
    assert res_clean.returncode == 0, f"Script failed on clean corpus: {res_clean.stderr}"

    # Run on evil corpus
    res_evil = subprocess.run(
        ["python3", SCRIPT_PATH, "--corpus", EVIL_CORPUS, "--video", VIDEO_PATH, "--out", EVIL_OUT],
        capture_output=True, text=True
    )
    assert res_evil.returncode == 0, f"Script failed on evil corpus: {res_evil.stderr}"

def test_clean_corpus_results():
    assert os.path.isfile(CLEAN_OUT), f"Output JSON for clean corpus not found at {CLEAN_OUT}"

    with open(CLEAN_OUT, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Clean results output is not valid JSON")

    expected_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith(".patch")]

    modified_clean = []
    missing_clean = []

    for fname in expected_files:
        if fname not in results:
            missing_clean.append(fname)
        elif results[fname] != "clean":
            modified_clean.append(fname)

    errors = []
    if missing_clean:
        errors.append(f"{len(missing_clean)} clean files missing from output: {missing_clean}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(expected_files)} clean modified/flagged as evil: {modified_clean}")

    if errors:
        pytest.fail("; ".join(errors))

def test_evil_corpus_results():
    assert os.path.isfile(EVIL_OUT), f"Output JSON for evil corpus not found at {EVIL_OUT}"

    with open(EVIL_OUT, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Evil results output is not valid JSON")

    expected_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith(".patch")]

    bypassed_evil = []
    missing_evil = []

    for fname in expected_files:
        if fname not in results:
            missing_evil.append(fname)
        elif results[fname] != "evil":
            bypassed_evil.append(fname)

    errors = []
    if missing_evil:
        errors.append(f"{len(missing_evil)} evil files missing from output: {missing_evil}")
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(expected_files)} evil bypassed/flagged as clean: {bypassed_evil}")

    if errors:
        pytest.fail("; ".join(errors))