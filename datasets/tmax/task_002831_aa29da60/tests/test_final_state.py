# test_final_state.py

import os
import subprocess
import tempfile
import pytest

EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"
MINITAR_BIN = "/app/minitar-0.1/minitar"
WATCH_SCRIPT = "/app/watch_and_extract.sh"

def test_minitar_binary_exists():
    assert os.path.isfile(MINITAR_BIN), f"Expected binary {MINITAR_BIN} is missing. Did you compile it?"
    assert os.access(MINITAR_BIN, os.X_OK), f"Expected {MINITAR_BIN} to be executable."

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} missing."
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} missing."

    evil_files = sorted([f for f in os.listdir(EVIL_DIR) if f.endswith(".tar")])
    clean_files = sorted([f for f in os.listdir(CLEAN_DIR) if f.endswith(".tar")])

    assert evil_files, "No evil tar files found."
    assert clean_files, "No clean tar files found."

    evil_bypassed = []
    clean_modified = []  # Using 'modified' to represent rejected/failed clean files per instructions

    with tempfile.TemporaryDirectory() as tmpdir:
        for f in evil_files:
            archive_path = os.path.join(EVIL_DIR, f)
            cmd = [MINITAR_BIN, "-x", "-f", archive_path]
            result = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True)

            # Pass criterion: exit code 1, prints "REJECT: <filename>"
            # The prompt says <filename> but the example gives <archive_name>. We will check for "REJECT: " and the filename/path.
            if result.returncode != 1 or "REJECT:" not in result.stdout or (f not in result.stdout and archive_path not in result.stdout):
                evil_bypassed.append(f)

        for f in clean_files:
            archive_path = os.path.join(CLEAN_DIR, f)
            cmd = [MINITAR_BIN, "-x", "-f", archive_path]
            result = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True)

            # Pass criterion: exit code 0, prints "ACCEPT: <filename>"
            if result.returncode != 0 or "ACCEPT:" not in result.stdout or (f not in result.stdout and archive_path not in result.stdout):
                clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail("; ".join(errors))

def test_watch_script_exists():
    assert os.path.isfile(WATCH_SCRIPT), f"Expected script {WATCH_SCRIPT} is missing."
    # The script should be somewhat substantial
    assert os.path.getsize(WATCH_SCRIPT) > 10, f"{WATCH_SCRIPT} is empty or too short."