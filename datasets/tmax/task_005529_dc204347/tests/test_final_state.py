# test_final_state.py

import os
import stat
import pytest

PIPELINE_DIR = "/home/user/pipeline_binaries"
SUID_VIOLATORS_FILE = "/home/user/suid_violators.txt"
EXTRACTED_SBOX_FILE = "/home/user/extracted_sbox.bin"
MAX_DIFF_FILE = "/home/user/max_diff.txt"
RUST_PROJECT_DIR = "/home/user/ddt_analyzer"

def test_suid_violators_file():
    assert os.path.isfile(SUID_VIOLATORS_FILE), f"{SUID_VIOLATORS_FILE} does not exist."

    # Recompute the expected SUID violators from the actual directory state
    expected_violators = []
    if os.path.isdir(PIPELINE_DIR):
        for root, _, files in os.walk(PIPELINE_DIR):
            for f in files:
                path = os.path.join(root, f)
                if os.path.isfile(path) and (os.stat(path).st_mode & stat.S_ISUID):
                    expected_violators.append(path)
    expected_violators.sort()

    with open(SUID_VIOLATORS_FILE, "r") as f:
        actual_violators = [line.strip() for line in f if line.strip()]

    assert actual_violators == expected_violators, (
        f"Contents of {SUID_VIOLATORS_FILE} do not match the expected sorted list of SUID binaries.\n"
        f"Expected: {expected_violators}\n"
        f"Actual: {actual_violators}"
    )

def test_extracted_sbox_file():
    assert os.path.isfile(EXTRACTED_SBOX_FILE), f"{EXTRACTED_SBOX_FILE} does not exist."

    with open(EXTRACTED_SBOX_FILE, "rb") as f:
        data = f.read()

    assert len(data) == 256, f"{EXTRACTED_SBOX_FILE} must be exactly 256 bytes long, got {len(data)} bytes."

    # The expected S-box is the identity function (0 to 255) based on the setup
    expected_data = bytes(range(256))
    assert data == expected_data, f"The contents of {EXTRACTED_SBOX_FILE} do not match the expected CUSTOM_SBOX data."

def test_rust_project_exists():
    cargo_toml = os.path.join(RUST_PROJECT_DIR, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Rust project not found. Expected {cargo_toml} to exist."

def test_max_diff_file():
    assert os.path.isfile(MAX_DIFF_FILE), f"{MAX_DIFF_FILE} does not exist."

    with open(MAX_DIFF_FILE, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"{MAX_DIFF_FILE} must contain a single integer value, got: '{content}'"

    # For the identity S-box, the maximum differential uniformity is 256
    assert int(content) == 256, f"Expected maximum differential uniformity to be 256, but got {content}."