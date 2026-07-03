# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_rust_project_exists():
    cargo_toml = "/home/user/graph_filter/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Rust project not found at {cargo_toml}"

def test_adversarial_corpus():
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"
    cargo_toml = "/home/user/graph_filter/Cargo.toml"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(
            ["cargo", "run", "--manifest-path", cargo_toml, "--", f],
            capture_output=True
        )
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(
            ["cargo", "run", "--manifest-path", cargo_toml, "--", f],
            capture_output=True
        )
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))