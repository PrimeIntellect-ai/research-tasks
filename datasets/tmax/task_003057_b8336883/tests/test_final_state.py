# test_final_state.py

import os
import subprocess
import pytest

SAFEGUARD_SCRIPT = "/home/user/safeguard.py"
EVIL_CORPUS_DIR = "/app/test_data/evil"
CLEAN_CORPUS_DIR = "/app/test_data/clean"

def test_safeguard_script_exists():
    assert os.path.isfile(SAFEGUARD_SCRIPT), f"Missing safeguard script at {SAFEGUARD_SCRIPT}"

def test_adversarial_corpus_evaluation():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Missing evil corpus directory at {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Missing clean corpus directory at {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "Evil corpus is empty"
    assert len(clean_files) > 0, "Clean corpus is empty"

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", SAFEGUARD_SCRIPT, evil_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "REJECT":
            evil_bypassed.append((os.path.basename(evil_file), output))

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", SAFEGUARD_SCRIPT, clean_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ACCEPT":
            clean_rejected.append((os.path.basename(clean_file), output))

    error_messages = []
    if evil_bypassed:
        basenames = [f[0] for f in evil_bypassed]
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(basenames)}")

    if clean_rejected:
        basenames = [f[0] for f in clean_rejected]
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(basenames)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))