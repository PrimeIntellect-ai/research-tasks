# test_final_state.py

import os
import subprocess
import pytest

SANITIZER_SCRIPT = "/home/user/sanitizer.py"
CLEAN_DIR = "/app/data/clean"
EVIL_DIR = "/app/data/evil"

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_SCRIPT), f"Sanitizer script not found at {SANITIZER_SCRIPT}"
    assert os.access(SANITIZER_SCRIPT, os.R_OK), f"Sanitizer script is not readable."

def test_sanitizer_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean directory missing: {CLEAN_DIR}"

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith(".json")]
    assert len(clean_files) > 0, "No clean JSON files found."

    modified_clean = []

    for file_path in clean_files:
        result = subprocess.run(
            ["python3", SANITIZER_SCRIPT, file_path],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if result.returncode != 0 or output != "SAFE":
            modified_clean.append(os.path.basename(file_path))

    if modified_clean:
        pytest.fail(f"{len(modified_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(modified_clean)}")

def test_sanitizer_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil directory missing: {EVIL_DIR}"

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith(".json")]
    assert len(evil_files) > 0, "No evil JSON files found."

    bypassed_evil = []

    for file_path in evil_files:
        result = subprocess.run(
            ["python3", SANITIZER_SCRIPT, file_path],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if result.returncode != 1 or output != "UNSAFE":
            bypassed_evil.append(os.path.basename(file_path))

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed/accepted. Offending files: {', '.join(bypassed_evil)}")