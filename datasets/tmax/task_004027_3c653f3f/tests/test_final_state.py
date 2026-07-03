# test_final_state.py

import os
import hashlib
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_rust_project_exists():
    manifest_builder_dir = "/home/user/manifest_builder"
    cargo_toml = os.path.join(manifest_builder_dir, "Cargo.toml")

    assert os.path.isdir(manifest_builder_dir), f"Rust project directory {manifest_builder_dir} is missing."
    assert os.path.isfile(cargo_toml), f"Cargo.toml is missing in {manifest_builder_dir}."

def test_manifest_file_correctness():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    # The three unique regular files we expect to be processed
    expected_files = [
        "/home/user/project_data/docs/readme.txt",
        "/home/user/project_data/assets/blob.bin",
        "/home/user/project_data/src/main.rs"
    ]

    expected_lines = []
    for f in expected_files:
        assert os.path.exists(f), f"Expected test file {f} is missing, environment might be corrupted."
        real_path = os.path.realpath(f)
        sha_hex = get_sha256(real_path)
        expected_lines.append(f"{sha_hex}  {real_path}")

    # Sort lines alphabetically by the canonical absolute path
    # Since the format is "<HASH>  <PATH>", and hashes are same length, sorting by the whole line
    # might sort by hash first. The instructions say "sorted alphabetically by the canonical absolute path".
    expected_lines.sort(key=lambda line: line.split("  ")[1])

    with open(manifest_path, "r") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Manifest has {len(actual_lines)} lines, expected {len(expected_lines)}. "
        "Ensure symlinks are deduplicated and loops are avoided."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: '{expected}'\nActual:   '{actual}'"