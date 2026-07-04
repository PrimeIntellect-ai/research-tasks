# test_final_state.py

import os
import subprocess
import pytest

def test_vendored_package_fixed():
    cargo_toml = "/app/vendored/log-parser-1.0.0/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}."

    with open(cargo_toml, "r") as f:
        content = f.read()
        assert "[dependencies]" in content, "Cargo.toml does not contain the fixed '[dependencies]' section."
        assert "[dependecies]" not in content, "Cargo.toml still contains the typo '[dependecies]'."

def test_detector_binary_exists():
    binary_path = "/home/user/detector/target/release/detector"
    assert os.path.isfile(binary_path), f"Detector binary not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Detector binary at {binary_path} is not executable."

def test_adversarial_corpus():
    binary_path = "/home/user/detector/target/release/detector"
    evil_dir = "/app/data/evil"
    clean_dir = "/app/data/clean"

    assert os.path.isdir(evil_dir), f"Evil data directory {evil_dir} does not exist."
    assert os.path.isdir(clean_dir), f"Clean data directory {clean_dir} does not exist."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        result = subprocess.run([binary_path, file_path], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(f)

    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        result = subprocess.run([binary_path, file_path], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(f)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)