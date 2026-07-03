# test_final_state.py
import os
import subprocess
import shutil
import pytest

SCRIPT_PATH = "/home/user/filter.py"
CLEAN_DIR = "/home/user/data/clean"
EVIL_DIR = "/home/user/data/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_adversarial_corpus():
    out_clean = "/tmp/out_clean_test"
    out_evil = "/tmp/out_evil_test"

    if os.path.exists(out_clean):
        shutil.rmtree(out_clean)
    if os.path.exists(out_evil):
        shutil.rmtree(out_evil)

    os.makedirs(out_clean)
    os.makedirs(out_evil)

    # Run script on clean corpus
    res_clean = subprocess.run(
        ["python3", SCRIPT_PATH, CLEAN_DIR, out_clean],
        capture_output=True, text=True
    )
    assert res_clean.returncode == 0, f"Script failed on clean corpus. Error:\n{res_clean.stderr}"

    # Run script on evil corpus
    res_evil = subprocess.run(
        ["python3", SCRIPT_PATH, EVIL_DIR, out_evil],
        capture_output=True, text=True
    )
    assert res_evil.returncode == 0, f"Script failed on evil corpus. Error:\n{res_evil.stderr}"

    # Analyze clean results
    clean_expected = set(os.listdir(CLEAN_DIR))
    clean_actual = set(os.listdir(out_clean))
    clean_missing = clean_expected - clean_actual

    # Analyze evil results
    evil_expected = set(os.listdir(EVIL_DIR))
    evil_actual = set(os.listdir(out_evil))
    evil_bypassed = evil_actual.intersection(evil_expected)

    errors = []
    if clean_missing:
        errors.append(f"{len(clean_missing)} of {len(clean_expected)} clean modified (missing from output): {', '.join(clean_missing)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_expected)} evil bypassed (copied to output): {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))