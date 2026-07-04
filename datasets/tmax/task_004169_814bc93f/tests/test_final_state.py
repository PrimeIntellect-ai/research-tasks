# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit_filter.py"
EVIL_DIR = "/home/user/corpora/evil"
CLEAN_DIR = "/home/user/corpora/clean"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The audit filter script was not found at {SCRIPT_PATH}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing at {EVIL_DIR}"

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "No evil files found to test."

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "VIOLATION":
                bypassed_files.append((filename, output))
        except subprocess.TimeoutExpired:
            bypassed_files.append((filename, "TIMEOUT"))
        except Exception as e:
            bypassed_files.append((filename, f"ERROR: {str(e)}"))

    if bypassed_files:
        details = ", ".join([f"{f} (got {out!r})" for f, out in bypassed_files])
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {details}")

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing at {CLEAN_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No clean files found to test."

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "SAFE":
                modified_files.append((filename, output))
        except subprocess.TimeoutExpired:
            modified_files.append((filename, "TIMEOUT"))
        except Exception as e:
            modified_files.append((filename, f"ERROR: {str(e)}"))

    if modified_files:
        details = ", ".join([f"{f} (got {out!r})" for f, out in modified_files])
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified/flagged: {details}")