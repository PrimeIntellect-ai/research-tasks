# test_final_state.py

import os
import glob
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/check_convergence.py"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} is not a file"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS, "*.h5"))
    assert len(clean_files) > 0, f"No .h5 files found in {CLEAN_CORPUS}"

    failed_files = []
    for f in clean_files:
        res = subprocess.run(["python3", AGENT_SCRIPT, f], capture_output=True)
        if res.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected): {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS, "*.h5"))
    assert len(evil_files) > 0, f"No .h5 files found in {EVIL_CORPUS}"

    bypassed_files = []
    for f in evil_files:
        res = subprocess.run(["python3", AGENT_SCRIPT, f], capture_output=True)
        # The prompt specifies that evil files should exit with 1
        if res.returncode != 1:
            bypassed_files.append(os.path.basename(f))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted): {', '.join(bypassed_files)}")