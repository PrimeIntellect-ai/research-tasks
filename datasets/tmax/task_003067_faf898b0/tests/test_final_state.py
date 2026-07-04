# test_final_state.py

import os
import subprocess
import pytest

SANITIZER_PATH = "/home/user/sanitizer"
CLEAN_DIR = "/home/user/corpora/clean"
EVIL_DIR = "/home/user/corpora/evil"

def test_sanitizer_exists_and_executable():
    assert os.path.isfile(SANITIZER_PATH), f"Compiled program not found at {SANITIZER_PATH}"
    assert os.access(SANITIZER_PATH, os.X_OK), f"Program at {SANITIZER_PATH} is not executable"

def test_clean_corpus():
    if not os.path.isfile(SANITIZER_PATH):
        pytest.fail("Sanitizer missing")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([SANITIZER_PATH, filepath], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "CLEAN":
            failed_files.append((os.path.basename(filepath), result.returncode, stdout))

    if failed_files:
        details = ", ".join([f"{f} (code {c}, out {o})" for f, c, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {details}")

def test_evil_corpus():
    if not os.path.isfile(SANITIZER_PATH):
        pytest.fail("Sanitizer missing")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([SANITIZER_PATH, filepath], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "EVIL":
            failed_files.append((os.path.basename(filepath), result.returncode, stdout))

    if failed_files:
        details = ", ".join([f"{f} (code {c}, out {o})" for f, c, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {details}")

def test_memory_leaks_valgrind():
    if not os.path.isfile(SANITIZER_PATH):
        pytest.fail("Sanitizer missing")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory"

    test_file = clean_files[0]

    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--show-leak-kinds=all",
        "--error-exitcode=42",
        SANITIZER_PATH,
        test_file
    ]

    try:
        result = subprocess.run(valgrind_cmd, capture_output=True, text=True)
    except FileNotFoundError:
        pytest.fail("valgrind is not installed or not in PATH")

    if result.returncode == 42:
        pytest.fail(f"Memory leak detected by valgrind on file {os.path.basename(test_file)}.\nValgrind output:\n{result.stderr}")

    # Double check stderr for definitely lost
    if "definitely lost:" in result.stderr:
        # Extract the definitely lost line
        for line in result.stderr.splitlines():
            if "definitely lost:" in line and " 0 bytes in 0 blocks" not in line:
                pytest.fail(f"Memory leak detected in valgrind output: {line.strip()}")