# test_final_state.py

import os
import subprocess
import pytest
from pathlib import Path

def test_filter_executable_exists():
    filter_path = "/home/user/filter"
    assert os.path.exists(filter_path), f"The executable {filter_path} does not exist. Did you compile your C++ code?"
    assert os.path.isfile(filter_path), f"{filter_path} is not a file."
    assert os.access(filter_path, os.X_OK), f"{filter_path} is not executable."

def test_adversarial_corpus():
    filter_path = "/home/user/filter"
    evil_dir = Path("/app/test_data/evil")
    clean_dir = Path("/app/test_data/clean")

    assert evil_dir.exists() and evil_dir.is_dir(), f"Evil corpus directory missing: {evil_dir}"
    assert clean_dir.exists() and clean_dir.is_dir(), f"Clean corpus directory missing: {clean_dir}"

    evil_files = list(evil_dir.glob("*"))
    clean_files = list(clean_dir.glob("*"))

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_rejected = []

    # Test evil corpus (expected exit code 1)
    for evil_file in evil_files:
        if not evil_file.is_file():
            continue
        try:
            result = subprocess.run([filter_path, str(evil_file)], capture_output=True, timeout=5)
            if result.returncode != 1:
                evil_bypassed.append((evil_file.name, result.returncode))
        except subprocess.TimeoutExpired:
            evil_bypassed.append((evil_file.name, "timeout"))

    # Test clean corpus (expected exit code 0)
    for clean_file in clean_files:
        if not clean_file.is_file():
            continue
        try:
            result = subprocess.run([filter_path, str(clean_file)], capture_output=True, timeout=5)
            if result.returncode != 0:
                clean_rejected.append((clean_file.name, result.returncode))
        except subprocess.TimeoutExpired:
            clean_rejected.append((clean_file.name, "timeout"))

    error_messages = []
    if evil_bypassed:
        bypassed_names = [f"{name} (exit code: {code})" for name, code in evil_bypassed]
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_names)}")

    if clean_rejected:
        rejected_names = [f"{name} (exit code: {code})" for name, code in clean_rejected]
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(rejected_names)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))