# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def test_detector_script_exists():
    detector_path = Path("/home/user/detector.py")
    assert detector_path.exists() and detector_path.is_file(), f"Detector script not found at {detector_path}"

def test_adversarial_corpus():
    detector_path = "/home/user/detector.py"
    evil_dir = Path("/app/corpus/evil")
    clean_dir = Path("/app/corpus/clean")

    assert evil_dir.exists() and evil_dir.is_dir(), f"Evil corpus directory missing: {evil_dir}"
    assert clean_dir.exists() and clean_dir.is_dir(), f"Clean corpus directory missing: {clean_dir}"

    evil_files = list(evil_dir.glob("*"))
    clean_files = list(clean_dir.glob("*"))

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_rejected = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", detector_path, str(evil_file)],
            capture_output=True,
            text=True
        )
        if result.returncode != 1 or "REJECT" not in result.stdout:
            evil_bypassed.append(evil_file.name)

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", detector_path, str(clean_file)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            clean_rejected.append(clean_file.name)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if errors:
        pytest.fail(" | ".join(errors))