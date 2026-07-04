# test_final_state.py
import os
import subprocess
import pytest

CRACKED_PASSWORD_PATH = "/home/user/cracked_password.txt"
SCRIPT_PATH = "/home/user/detect_backdoor.sh"
EVIL_CORPUS_PATH = "/app/corpora/evil"
CLEAN_CORPUS_PATH = "/app/corpora/clean"

def test_cracked_password():
    assert os.path.exists(CRACKED_PASSWORD_PATH), f"Missing cracked password file at {CRACKED_PASSWORD_PATH}"
    with open(CRACKED_PASSWORD_PATH, 'r') as f:
        content = f.read().strip()
    assert content == "dragon", f"Incorrect cracked password. Expected 'dragon', got '{content}'"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Missing detection script at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus_evil():
    if not os.path.exists(EVIL_CORPUS_PATH):
        pytest.fail(f"Evil corpus path {EVIL_CORPUS_PATH} does not exist.")

    evil_files = [os.path.join(EVIL_CORPUS_PATH, f) for f in os.listdir(EVIL_CORPUS_PATH) if os.path.isfile(os.path.join(EVIL_CORPUS_PATH, f))]
    if not evil_files:
        pytest.fail(f"No files found in evil corpus at {EVIL_CORPUS_PATH}")

    bypassed_files = []

    for file_path in evil_files:
        result = subprocess.run([SCRIPT_PATH, file_path], capture_output=True, text=True)
        stdout = result.stdout.strip()

        if result.returncode != 1 or stdout != "EVIL":
            bypassed_files.append(os.path.basename(file_path))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_adversarial_corpus_clean():
    if not os.path.exists(CLEAN_CORPUS_PATH):
        pytest.fail(f"Clean corpus path {CLEAN_CORPUS_PATH} does not exist.")

    clean_files = [os.path.join(CLEAN_CORPUS_PATH, f) for f in os.listdir(CLEAN_CORPUS_PATH) if os.path.isfile(os.path.join(CLEAN_CORPUS_PATH, f))]
    if not clean_files:
        pytest.fail(f"No files found in clean corpus at {CLEAN_CORPUS_PATH}")

    modified_files = []

    for file_path in clean_files:
        result = subprocess.run([SCRIPT_PATH, file_path], capture_output=True, text=True)
        stdout = result.stdout.strip()

        if result.returncode != 0 or stdout != "CLEAN":
            modified_files.append(os.path.basename(file_path))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified. Offending files: {', '.join(modified_files)}")