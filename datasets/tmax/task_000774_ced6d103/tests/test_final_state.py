# test_final_state.py
import os
import subprocess
import pytest

EVIL_DIR = "/hidden/eval_corpus/blocked"
CLEAN_DIR = "/hidden/eval_corpus/allowed"
SCRIPT_PATH = "/home/user/offline_ids.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Missing evil corpus dir: {EVIL_DIR}"
    assert os.path.isdir(CLEAN_DIR), f"Missing clean corpus dir: {CLEAN_DIR}"

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, f"No files in evil corpus at {EVIL_DIR}."
    assert len(clean_files) > 0, f"No files in clean corpus at {CLEAN_DIR}."

    bypassed_evil = []
    for f in evil_files:
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, f],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "BLOCKED":
                bypassed_evil.append((os.path.basename(f), output))
        except Exception as e:
            bypassed_evil.append((os.path.basename(f), f"Error: {str(e)}"))

    modified_clean = []
    for f in clean_files:
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, f],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "ALLOWED":
                modified_clean.append((os.path.basename(f), output))
        except Exception as e:
            modified_clean.append((os.path.basename(f), f"Error: {str(e)}"))

    error_msg = []
    if bypassed_evil:
        error_msg.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: " + ", ".join([x[0] for x in bypassed_evil]))
    if modified_clean:
        error_msg.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: " + ", ".join([x[0] for x in modified_clean]))

    assert not bypassed_evil and not modified_clean, " | ".join(error_msg)