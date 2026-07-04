# test_final_state.py

import os
import subprocess
import pytest

WAF_SCRIPT = "/home/user/waf.py"
CLEAN_CORPUS_DIR = "/app/traffic/clean/"
EVIL_CORPUS_DIR = "/app/traffic/evil/"

def test_waf_script_exists():
    """Ensure the student created the WAF script at the correct location."""
    assert os.path.exists(WAF_SCRIPT), f"WAF script not found at {WAF_SCRIPT}"
    assert os.path.isfile(WAF_SCRIPT), f"{WAF_SCRIPT} is not a file"

def test_waf_against_clean_corpus():
    """
    Iterate over every file in the clean corpus path and assert the agent's 
    solution leaves it unchanged / accepted (exit code 0, prints CLEAN).
    """
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus directory is empty."

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)

        result = subprocess.run(
            ["python3", WAF_SCRIPT, filepath],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or "CLEAN" not in result.stdout:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean requests modified/rejected. Offending files: {', '.join(failed_files)}")

def test_waf_against_evil_corpus():
    """
    Iterate over every file in the evil corpus path and assert the agent's 
    solution rejects each one (exit code 1, prints EVIL).
    """
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus directory is empty."

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)

        result = subprocess.run(
            ["python3", WAF_SCRIPT, filepath],
            capture_output=True,
            text=True
        )

        if result.returncode != 1 or "EVIL" not in result.stdout:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil requests bypassed. Offending files: {', '.join(failed_files)}")