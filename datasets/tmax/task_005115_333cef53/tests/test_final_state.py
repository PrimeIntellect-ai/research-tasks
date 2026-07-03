# test_final_state.py

import os
import subprocess
import pytest

def test_root_finder_pkg_installed():
    try:
        import root_finder_pkg
    except ImportError:
        pytest.fail("root_finder_pkg is not installed or cannot be imported. Did you fix setup.py and install it?")

def test_sanitizer_adversarial_corpus():
    sanitizer_script = '/home/user/sanitizer.py'
    assert os.path.isfile(sanitizer_script), f"Sanitizer script missing at {sanitizer_script}"

    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.npz')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.npz')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        result = subprocess.run(['python', sanitizer_script, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run(['python', sanitizer_script, ef], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))