# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_validate_executable_exists():
    executable = "/home/user/validate"
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_adversarial_corpus():
    executable = "/home/user/validate"
    video_path = "/app/test_sequence.mp4"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = sorted(glob.glob(os.path.join(clean_dir, "*")))
    evil_files = sorted(glob.glob(os.path.join(evil_dir, "*")))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_rejected = []
    for clean_file in clean_files:
        result = subprocess.run([executable, video_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([executable, video_path, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")

    if errors:
        pytest.fail(" | ".join(errors))