# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def test_video_analyzer_output():
    """Test that the video signal analyzer correctly identified the black frames."""
    output_file = Path("/home/user/dropouts.txt")
    assert output_file.is_file(), f"Expected output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = f.read().splitlines()

    # Remove any empty lines
    lines = [line.strip() for line in lines if line.strip()]

    # Expected frame indices from ground truth
    expected_frames = ["42", "43", "44", "89"]

    assert lines == expected_frames, f"Expected frames {expected_frames}, but got {lines}."

def test_adversarial_corpus():
    """Test that the Rust binary correctly accepts clean payloads and rejects evil payloads."""
    binary_path = Path("/home/user/edge_filter/target/release/edge_filter")
    assert binary_path.is_file(), f"Rust binary not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable."

    clean_dir = Path("/app/corpora/clean")
    evil_dir = Path("/app/corpora/evil")

    assert clean_dir.is_dir(), f"Clean corpus directory missing: {clean_dir}"
    assert evil_dir.is_dir(), f"Evil corpus directory missing: {evil_dir}"

    clean_files = list(clean_dir.glob("*.json"))
    evil_files = list(evil_dir.glob("*.json"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for clean_file in clean_files:
        result = subprocess.run([str(binary_path), str(clean_file)], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(clean_file.name)

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([str(binary_path), str(evil_file)], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(evil_file.name)

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    assert not errors, "Adversarial corpus verification failed: " + "; ".join(errors)

def test_deploy_script_exists():
    """Test that the deployment script was created."""
    deploy_script = Path("/home/user/deploy.sh")
    assert deploy_script.is_file(), f"Deployment script not found at {deploy_script}."