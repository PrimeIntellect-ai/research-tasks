# test_final_state.py
import os
import subprocess
import glob

SCRIPT_PATH = "/home/user/check_payload.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    # Ensure script exists
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    clean_failures = []
    evil_failures = []

    # Test clean corpus (should exit 0)
    for file_path in clean_files:
        result = subprocess.run([SCRIPT_PATH, file_path], capture_output=True)
        if result.returncode != 0:
            clean_failures.append((os.path.basename(file_path), result.returncode))

    # Test evil corpus (should exit 1)
    for file_path in evil_files:
        result = subprocess.run([SCRIPT_PATH, file_path], capture_output=True)
        if result.returncode != 1:
            evil_failures.append((os.path.basename(file_path), result.returncode))

    error_messages = []
    if evil_failures:
        bypassed_files = [f[0] for f in evil_failures]
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {bypassed_files}")

    if clean_failures:
        modified_files = [f[0] for f in clean_failures]
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {modified_files}")

    if error_messages:
        assert False, " | ".join(error_messages)