# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    cargo_toml = "/home/user/archiver/Cargo.toml"
    main_rs = "/home/user/archiver/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project not found: {cargo_toml} is missing."
    assert os.path.isfile(main_rs), f"Rust source file not found: {main_rs} is missing."

def test_archive_manifest_exists():
    manifest_path = "/home/user/archive_manifest.csv"
    assert os.path.isfile(manifest_path), f"Output file {manifest_path} was not created."

def test_archive_manifest_content():
    manifest_path = "/home/user/archive_manifest.csv"

    expected_lines = [
        "/etc/hostname,27",
        "/var/log/auth.log,6735",
        "/home/user/.bashrc,3700"
    ]

    with open(manifest_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in manifest, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual.strip()}'."