# test_final_state.py

import os
import subprocess
import fcntl
from pathlib import Path
import pytest

CLEAN_CORPUS = Path("/app/corpus/clean/")
EVIL_CORPUS = Path("/app/corpus/evil/")
SCRIPT_PATH = Path("/home/user/validate_doc_archive.sh")
REFERENCE_FRAME = Path("/home/user/reference_frame.jpg")

def test_reference_frame_extracted():
    assert REFERENCE_FRAME.exists(), f"Missing extracted reference frame at {REFERENCE_FRAME}"
    assert REFERENCE_FRAME.is_file(), f"{REFERENCE_FRAME} is not a file"
    assert REFERENCE_FRAME.stat().st_size > 0, f"{REFERENCE_FRAME} is empty"

def test_script_exists_and_executable():
    assert SCRIPT_PATH.exists(), f"Missing script at {SCRIPT_PATH}"
    assert SCRIPT_PATH.is_file(), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_clean_corpus():
    clean_files = list(CLEAN_CORPUS.glob("*.tar.gz"))
    assert len(clean_files) > 0, "No clean archives found to test."

    failed_clean = []
    for archive in clean_files:
        result = subprocess.run(
            ["timeout", "5", str(SCRIPT_PATH), str(archive)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_clean.append(archive.name)

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}"

def test_evil_corpus():
    evil_files = list(EVIL_CORPUS.glob("*.tar.gz"))
    assert len(evil_files) > 0, "No evil archives found to test."

    failed_evil = []

    for archive in evil_files:
        lock_file = archive.with_name(archive.name + ".lock")
        lock_fd = None

        # Simulate lock held by background process for evil_1.tar.gz
        if archive.name == "evil_1.tar.gz":
            lock_fd = open(lock_file, "w")
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                pass # Already locked

        try:
            result = subprocess.run(
                ["timeout", "5", str(SCRIPT_PATH), str(archive)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # We expect a non-zero exit code for evil archives
            if result.returncode == 0:
                failed_evil.append(archive.name)
        finally:
            if lock_fd:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()
                if lock_file.exists():
                    try:
                        lock_file.unlink()
                    except OSError:
                        pass

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}"