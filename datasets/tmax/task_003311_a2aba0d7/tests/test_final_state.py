# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def test_perturbations_fixed():
    """Verify that the deliberate perturbations in the vendored package have been fixed."""
    makefile_path = Path("/app/bash-ds-utils/Makefile")
    assert makefile_path.is_file(), "Makefile is missing."
    makefile_content = makefile_path.read_text()
    assert "CC=/usr/bin/false" not in makefile_content, "Makefile still contains the perturbation 'CC=/usr/bin/false'."

    setup_env_path = Path("/app/bash-ds-utils/setup_env.sh")
    assert setup_env_path.is_file(), "setup_env.sh is missing."
    setup_env_content = setup_env_path.read_text()
    assert "TRACKER_HOME=/nonexistent" not in setup_env_content, "setup_env.sh still contains the perturbation 'TRACKER_HOME=/nonexistent'."

def test_track_exp_compiled():
    """Verify that the track_exp binary has been compiled successfully."""
    track_exp = Path("/app/bash-ds-utils/bin/track_exp")
    assert track_exp.is_file(), "track_exp binary was not compiled. Did you run 'make install'?"
    assert os.access(track_exp, os.X_OK), "track_exp binary is not executable."

def test_filter_script_exists():
    """Verify that the filter.sh script exists and is executable."""
    filter_script = Path("/home/user/filter.sh")
    assert filter_script.is_file(), "filter.sh script does not exist at /home/user/filter.sh."
    assert os.access(filter_script, os.X_OK), "filter.sh script is not executable."

def test_adversarial_corpus():
    """Verify that filter.sh correctly accepts clean files and rejects evil files."""
    filter_script = Path("/home/user/filter.sh")
    clean_dir = Path("/home/user/data/clean")
    evil_dir = Path("/home/user/data/evil")

    assert clean_dir.is_dir(), f"Clean corpus directory {clean_dir} missing."
    assert evil_dir.is_dir(), f"Evil corpus directory {evil_dir} missing."

    clean_files = list(clean_dir.glob("*"))
    evil_files = list(evil_dir.glob("*"))

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_bypassed = []
    evil_bypassed = []

    for f in clean_files:
        res = subprocess.run([str(filter_script), str(f)], capture_output=True)
        if res.returncode != 0:
            clean_bypassed.append(f.name)

    for f in evil_files:
        res = subprocess.run([str(filter_script), str(f)], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(f.name)

    errors = []
    if clean_bypassed:
        errors.append(f"{len(clean_bypassed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_bypassed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)