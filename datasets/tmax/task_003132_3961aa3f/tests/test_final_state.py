# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/artifact_filter.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} is not executable"

def test_clean_corpus():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_CORPUS_DIR} does not exist.")

    artifacts = [d for d in os.listdir(CLEAN_CORPUS_DIR) if os.path.isdir(os.path.join(CLEAN_CORPUS_DIR, d))]
    if not artifacts:
        pytest.skip(f"No artifacts found in {CLEAN_CORPUS_DIR}.")

    failed_artifacts = []

    for artifact in artifacts:
        artifact_path = os.path.join(CLEAN_CORPUS_DIR, artifact)
        result = subprocess.run([SCRIPT_PATH, artifact_path], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            failed_artifacts.append((artifact, output))

    if failed_artifacts:
        summary = f"{len(failed_artifacts)} of {len(artifacts)} clean modified/rejected. "
        details = ", ".join([f"{a} (output: {o})" for a, o in failed_artifacts])
        pytest.fail(f"{summary}Offending artifacts: {details}")

def test_evil_corpus():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_CORPUS_DIR} does not exist.")

    artifacts = [d for d in os.listdir(EVIL_CORPUS_DIR) if os.path.isdir(os.path.join(EVIL_CORPUS_DIR, d))]
    if not artifacts:
        pytest.skip(f"No artifacts found in {EVIL_CORPUS_DIR}.")

    failed_artifacts = []

    for artifact in artifacts:
        artifact_path = os.path.join(EVIL_CORPUS_DIR, artifact)
        result = subprocess.run([SCRIPT_PATH, artifact_path], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            failed_artifacts.append((artifact, output))

    if failed_artifacts:
        summary = f"{len(failed_artifacts)} of {len(artifacts)} evil bypassed. "
        details = ", ".join([f"{a} (output: {o})" for a, o in failed_artifacts])
        pytest.fail(f"{summary}Offending artifacts: {details}")