# test_final_state.py

import os
import subprocess
import pytest

SAFEGUARD_SCRIPT = "/home/user/safeguard.sh"
EVIL_CORPUS = "/home/user/corpus/evil"
CLEAN_CORPUS = "/home/user/corpus/clean"

def test_safeguard_exists_and_executable():
    assert os.path.isfile(SAFEGUARD_SCRIPT), f"Safeguard script is missing: {SAFEGUARD_SCRIPT}"
    assert os.access(SAFEGUARD_SCRIPT, os.X_OK), f"Safeguard script is not executable: {SAFEGUARD_SCRIPT}"

def test_clean_corpus_accepted():
    if not os.path.isfile(SAFEGUARD_SCRIPT):
        pytest.fail("Safeguard script does not exist.")

    failures = []
    files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    total = len(files)

    for f in files:
        path = os.path.join(CLEAN_CORPUS, f)
        res = subprocess.run([SAFEGUARD_SCRIPT, path], capture_output=True, text=True)
        out = res.stdout.strip()

        if res.returncode != 0 or out != "ACCEPT":
            failures.append(f)

    if failures:
        pytest.fail(f"{len(failures)} of {total} clean files rejected or improperly handled. Offending files: {', '.join(failures)}")

def test_evil_corpus_rejected():
    if not os.path.isfile(SAFEGUARD_SCRIPT):
        pytest.fail("Safeguard script does not exist.")

    failures = []
    files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    total = len(files)

    for f in files:
        path = os.path.join(EVIL_CORPUS, f)
        res = subprocess.run([SAFEGUARD_SCRIPT, path], capture_output=True, text=True)
        out = res.stdout.strip()

        if res.returncode != 1 or out != "REJECT":
            failures.append(f)

    if failures:
        pytest.fail(f"{len(failures)} of {total} evil files bypassed validation. Offending files: {', '.join(failures)}")