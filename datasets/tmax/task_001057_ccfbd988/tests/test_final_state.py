# test_final_state.py
import os
import subprocess
import fcntl
import pytest

CLEAN_DIR = '/app/corpus/clean'
EVIL_DIR = '/app/corpus/evil'
EXECUTABLE = '/home/user/config_filter'

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([EXECUTABLE, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run([EXECUTABLE, f], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)

def test_file_locking():
    """Verify that the program fails to run if the lock file is already held."""
    lock_file = '/tmp/config_filter.lock'

    # Get a valid clean file to test with
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No clean files available for lock testing."
    test_file = clean_files[0]

    # Hold the lock in Python
    with open(lock_file, 'w') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_acquired = True
        except BlockingIOError:
            lock_acquired = False

        assert lock_acquired, "Test setup failed: could not acquire lock."

        # Run the executable, it should fail because the lock is held
        result = subprocess.run([EXECUTABLE, test_file], capture_output=True)

        # Release the lock
        fcntl.flock(f, fcntl.LOCK_UN)

    assert result.returncode != 0, "Executable bypassed file locking: it succeeded even when the lock was held by another process."