# test_final_state.py

import os
import subprocess
import zipfile
import tarfile
import pytest

SCRIPT_PATH = "/home/user/storage_cleaner.py"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    # Run on clean corpus
    res_clean = subprocess.run(["python3", SCRIPT_PATH, CLEAN_DIR], capture_output=True, text=True)
    assert res_clean.returncode == 0, f"Script failed on clean corpus:\nSTDOUT: {res_clean.stdout}\nSTDERR: {res_clean.stderr}"

    # Run on evil corpus
    res_evil = subprocess.run(["python3", SCRIPT_PATH, EVIL_DIR], capture_output=True, text=True)
    assert res_evil.returncode == 0, f"Script failed on evil corpus:\nSTDOUT: {res_evil.stdout}\nSTDERR: {res_evil.stderr}"

def test_clean_corpus_unmodified():
    # Check valid_archive.zip
    valid_zip = os.path.join(CLEAN_DIR, "valid_archive.zip")
    assert os.path.isfile(valid_zip), "Clean corpus: valid_archive.zip was incorrectly deleted."
    assert zipfile.is_zipfile(valid_zip), "Clean corpus: valid_archive.zip was corrupted."

    # Check safe_link
    safe_link = os.path.join(CLEAN_DIR, "safe_link")
    assert os.path.islink(safe_link), "Clean corpus: safe_link was incorrectly deleted or modified."

    # Check app.log
    app_log = os.path.join(CLEAN_DIR, "app.log")
    assert os.path.isfile(app_log), "Clean corpus: app.log was incorrectly deleted."
    with open(app_log, "r") as f:
        content = f.read()
        assert "[REDACTED]" not in content, "Clean corpus: app.log was incorrectly redacted."

def test_evil_corpus_sanitized():
    # Check corrupt_archive.zip
    corrupt_zip = os.path.join(EVIL_DIR, "corrupt_archive.zip")
    assert not os.path.exists(corrupt_zip), "Evil corpus: corrupt_archive.zip was not deleted."

    # Check loop_dir/infinite
    infinite_link = os.path.join(EVIL_DIR, "loop_dir", "infinite")
    assert not os.path.exists(infinite_link), "Evil corpus: infinite symlink was not deleted."

    # Check error.log
    error_log = os.path.join(EVIL_DIR, "error.log")
    assert os.path.isfile(error_log), "Evil corpus: error.log was deleted instead of redacted."
    with open(error_log, "r") as f:
        content = f.read()
        assert "ERR9X" not in content, "Evil corpus: error.log still contains the error code ERR9X."
        assert "[REDACTED]" in content, "Evil corpus: error.log does not contain [REDACTED] replacements."