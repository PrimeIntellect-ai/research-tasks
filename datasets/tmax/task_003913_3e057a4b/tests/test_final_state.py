# test_final_state.py

import os
import subprocess
import pytest

EVIL_CORPUS = "/app/corpora/evil/"
CLEAN_CORPUS = "/app/corpora/clean/"
SANITIZER_BIN = "/home/user/sanitizer"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
REPO_PATH = "/home/user/packetd_repo"

def test_sanitizer_exists_and_executable():
    assert os.path.isfile(SANITIZER_BIN), f"Sanitizer binary not found at {SANITIZER_BIN}"
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary at {SANITIZER_BIN} is not executable"

def test_sanitizer_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS):
        pytest.skip("Evil corpus directory not found")

    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert evil_files, "Evil corpus is empty"

    bypassed = []
    for filepath in evil_files:
        with open(filepath, 'rb') as f:
            payload = f.read()
        try:
            result = subprocess.run([SANITIZER_BIN], input=payload, capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "0":
                bypassed.append(os.path.basename(filepath))
        except Exception as e:
            bypassed.append(f"{os.path.basename(filepath)} (error: {e})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil payloads bypassed the sanitizer: {', '.join(bypassed[:5])}")

def test_sanitizer_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS):
        pytest.skip("Clean corpus directory not found")

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert clean_files, "Clean corpus is empty"

    modified = []
    for filepath in clean_files:
        with open(filepath, 'rb') as f:
            payload = f.read()
        try:
            result = subprocess.run([SANITIZER_BIN], input=payload, capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "1":
                modified.append(os.path.basename(filepath))
        except Exception as e:
            modified.append(f"{os.path.basename(filepath)} (error: {e})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean payloads were rejected: {', '.join(modified[:5])}")

def test_bad_commit_identified():
    assert os.path.isfile(BAD_COMMIT_FILE), f"Bad commit file not found at {BAD_COMMIT_FILE}"

    with open(BAD_COMMIT_FILE, 'r') as f:
        student_commit = f.read().strip()

    assert student_commit, "Bad commit file is empty"

    # Verify it's a valid commit in the repo
    try:
        subprocess.check_output(["git", "cat-file", "-e", student_commit], cwd=REPO_PATH, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pytest.fail(f"The commit hash in {BAD_COMMIT_FILE} ({student_commit}) is not a valid commit in the repository.")