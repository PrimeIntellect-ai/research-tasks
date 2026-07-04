# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_executable_exists():
    """Test that the student's executable exists and is executable."""
    executable = "/home/user/filter_backup"
    assert os.path.isfile(executable), f"Executable not found at {executable}."
    assert os.access(executable, os.X_OK), f"File at {executable} is not executable."

def test_adversarial_corpus():
    """Test the executable against the clean and evil corpora."""
    executable = "/home/user/filter_backup"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for file in clean_files:
        try:
            # We add LD_LIBRARY_PATH just in case the student didn't bake it into the executable
            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = "/app/libgraphbackup-1.2.0/build/lib:" + env.get("LD_LIBRARY_PATH", "")

            result = subprocess.run(
                [executable, file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env
            )
            if result.returncode != 0:
                clean_failures.append(os.path.basename(file))
        except Exception as e:
            clean_failures.append(f"{os.path.basename(file)} (error: {e})")

    evil_failures = []
    for file in evil_files:
        try:
            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = "/app/libgraphbackup-1.2.0/build/lib:" + env.get("LD_LIBRARY_PATH", "")

            result = subprocess.run(
                [executable, file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env
            )
            if result.returncode != 1:
                evil_failures.append(os.path.basename(file))
        except Exception as e:
            evil_failures.append(f"{os.path.basename(file)} (error: {e})")

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures[:5])}{'...' if len(clean_failures)>5 else ''}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures[:5])}{'...' if len(evil_failures)>5 else ''}")

    assert not clean_failures and not evil_failures, " | ".join(error_messages)