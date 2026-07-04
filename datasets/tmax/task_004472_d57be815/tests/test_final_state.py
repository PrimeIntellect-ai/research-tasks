# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/clean_and_backup.py"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"
SUMMARY_PATH = "/home/user/backup_summary.txt"

@pytest.fixture(scope="session", autouse=True)
def execute_student_script():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    # Run on clean corpus
    try:
        subprocess.run(["python3", SCRIPT_PATH, CLEAN_CORPUS], check=True, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        pytest.fail("Script timed out on clean corpus.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed on clean corpus:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

    # Run on evil corpus
    try:
        subprocess.run(["python3", SCRIPT_PATH, EVIL_CORPUS], check=True, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        pytest.fail("Script timed out on evil corpus (likely infinite loop).")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed on evil corpus:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

def test_clean_corpus_preserved():
    assert os.path.exists(CLEAN_CORPUS), f"Clean corpus directory {CLEAN_CORPUS} is missing."
    items = os.listdir(CLEAN_CORPUS)
    assert len(items) > 0, "Clean corpus appears to be empty; files were incorrectly deleted."

    # Check that all links in clean corpus are valid
    for root, dirs, files in os.walk(CLEAN_CORPUS):
        for name in dirs + files:
            path = os.path.join(root, name)
            if os.path.islink(path):
                assert os.path.exists(path), f"Valid symlink {path} is broken or was incorrectly modified."

def test_evil_corpus_sanitized():
    assert os.path.exists(EVIL_CORPUS), f"Evil corpus directory {EVIL_CORPUS} is missing."

    # Check that NO cyclic symlinks remain in the evil corpus
    for root, dirs, files in os.walk(EVIL_CORPUS):
        for name in dirs + files:
            path = os.path.join(root, name)
            if os.path.islink(path):
                # If it's a link, it must not be cyclic.
                # Cyclic links will have os.path.exists() return False.
                assert os.path.exists(path), f"Cyclic or broken symlink {path} was not deleted."

def test_backup_summary_created_and_populated():
    assert os.path.exists(SUMMARY_PATH), f"Backup summary not found at {SUMMARY_PATH}"
    with open(SUMMARY_PATH, "r") as f:
        lines = f.readlines()

    # Count valid regular files in both corpora
    valid_files = 0
    for corpus in [CLEAN_CORPUS, EVIL_CORPUS]:
        for root, dirs, files in os.walk(corpus):
            for name in files:
                path = os.path.join(root, name)
                if os.path.isfile(path): # os.path.isfile resolves symlinks
                    valid_files += 1

    assert len(lines) == valid_files, f"Expected {valid_files} lines in summary, got {len(lines)}"