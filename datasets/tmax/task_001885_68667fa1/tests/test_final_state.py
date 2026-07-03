# test_final_state.py
import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/detect_slip.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
RED_FRAME_COUNT_FILE = "/home/user/red_frame_count.txt"
EXPECTED_RED_FRAMES = 34

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.manifest"))
    assert clean_files, f"No clean manifests found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for manifest in clean_files:
        result = subprocess.run([SCRIPT_PATH, manifest], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            failed_files.append(os.path.basename(manifest))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean manifests incorrectly flagged as EVIL or failed: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.manifest"))
    assert evil_files, f"No evil manifests found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for manifest in evil_files:
        result = subprocess.run([SCRIPT_PATH, manifest], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "EVIL":
            failed_files.append(os.path.basename(manifest))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil manifests bypassed detection: {', '.join(failed_files)}")

def test_red_frame_count():
    assert os.path.isfile(RED_FRAME_COUNT_FILE), f"Output file not found at {RED_FRAME_COUNT_FILE}"
    with open(RED_FRAME_COUNT_FILE, "r") as f:
        content = f.read().strip()

    try:
        count = int(content)
    except ValueError:
        pytest.fail(f"File {RED_FRAME_COUNT_FILE} contains non-integer value: {content}")

    assert count == EXPECTED_RED_FRAMES, f"Expected {EXPECTED_RED_FRAMES} red frames, but got {count}"