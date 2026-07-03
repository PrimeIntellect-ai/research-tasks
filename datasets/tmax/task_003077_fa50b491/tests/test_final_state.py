# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def test_validate_script_exists_and_executable():
    script_path = Path("/home/user/validate.sh")
    assert script_path.exists(), f"Script not found at {script_path}"
    assert script_path.is_file(), f"{script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_adversarial_corpus():
    script_path = "/home/user/validate.sh"

    evil_dir = Path("/app/evil")
    clean_dir = Path("/app/clean")

    evil_files = list(evil_dir.glob("*.csv"))
    clean_files = list(clean_dir.glob("*.csv"))

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    bypassed_evil = []
    for evil_file in evil_files:
        result = subprocess.run([script_path, str(evil_file)], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(evil_file.name)

    modified_clean = []
    for clean_file in clean_files:
        result = subprocess.run([script_path, str(clean_file)], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(clean_file.name)

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    assert not errors, " | ".join(errors)