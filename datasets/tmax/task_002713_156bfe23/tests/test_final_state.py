# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/policy_validator.py"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_policy_validator_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_policy_validator_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing at {CLEAN_CORPUS}"
    clean_files = sorted([f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.json')])
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, f)
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ALLOW" or result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (blocked or failed). Offending files: {', '.join(failed_files)}")

def test_policy_validator_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing at {EVIL_CORPUS}"
    evil_files = sorted([f for f in os.listdir(EVIL_CORPUS) if f.endswith('.json')])
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS, f)
        result = subprocess.run(["python3", SCRIPT_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "BLOCK" or result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")