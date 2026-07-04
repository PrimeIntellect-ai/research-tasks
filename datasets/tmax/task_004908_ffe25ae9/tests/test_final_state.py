# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/sanitiser"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
OUTPUT_FILE = "/tmp/output.jsonl"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_clean_corpus_preserved():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".jsonl")]
    assert clean_files, "No clean corpus files found."

    modified_files = []

    for filename in clean_files:
        input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

        result = subprocess.run([EXECUTABLE, input_path, OUTPUT_FILE], capture_output=True)
        if result.returncode != 0:
            modified_files.append((filename, f"Crashed with return code {result.returncode}"))
            continue

        if not os.path.exists(OUTPUT_FILE):
            modified_files.append((filename, "Output file not created"))
            continue

        with open(input_path, "rb") as f:
            expected_data = f.read()
        with open(OUTPUT_FILE, "rb") as f:
            actual_data = f.read()

        if expected_data != actual_data:
            modified_files.append((filename, "Output does not match input exactly"))

    if modified_files:
        details = "\n".join(f" - {f}: {reason}" for f, reason in modified_files)
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean files modified or failed:\n{details}")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".jsonl")]
    assert evil_files, "No evil corpus files found."

    bypassed_files = []

    for filename in evil_files:
        input_path = os.path.join(EVIL_CORPUS_DIR, filename)
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

        result = subprocess.run([EXECUTABLE, input_path, OUTPUT_FILE], capture_output=True)
        if result.returncode != 0:
            # Crashing on evil input is not ideal but counts as rejection if output is empty/non-existent
            pass

        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    bypassed_files.append((filename, "Output file is not empty"))

    if bypassed_files:
        details = "\n".join(f" - {f}: {reason}" for f, reason in bypassed_files)
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed validation:\n{details}")