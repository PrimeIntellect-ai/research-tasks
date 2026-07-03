# test_final_state.py

import os
import json
import hashlib
import pytest

def get_file_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_curated_artifacts_directory_exists():
    curated_dir = "/home/user/curated_artifacts"
    assert os.path.isdir(curated_dir), f"Directory {curated_dir} does not exist."

def test_reconstructed_artifacts():
    manifest_path = "/home/user/manifest.json"
    raw_chunks_dir = "/home/user/raw_chunks"
    curated_dir = "/home/user/curated_artifacts"
    log_file = os.path.join(curated_dir, "integrity_failures.log")

    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    expected_failures = []

    for artifact in manifest.get("artifacts", []):
        canonical_name = artifact["canonical_name"]
        expected_sha256 = artifact["expected_sha256"]
        chunks = artifact["chunks"]

        # Reconstruct from raw chunks to see if it's corrupt
        merged_data = b""
        for chunk_name in chunks:
            chunk_path = os.path.join(raw_chunks_dir, chunk_name)
            with open(chunk_path, "rb") as cf:
                merged_data += cf.read()

        actual_sha256 = hashlib.sha256(merged_data).hexdigest()

        artifact_path = os.path.join(curated_dir, canonical_name)

        if actual_sha256 == expected_sha256:
            # Should be successfully reconstructed
            assert os.path.isfile(artifact_path), f"Valid artifact {canonical_name} was not saved to {curated_dir}."
            saved_sha256 = get_file_sha256(artifact_path)
            assert saved_sha256 == expected_sha256, f"Checksum mismatch for {canonical_name}. Expected {expected_sha256}, got {saved_sha256}."
        else:
            # Should be marked as corrupt
            assert not os.path.isfile(artifact_path), f"Corrupt artifact {canonical_name} should not have been saved to {curated_dir}."
            expected_failures.append(canonical_name)

    # Check integrity_failures.log
    if expected_failures:
        assert os.path.isfile(log_file), f"Log file {log_file} does not exist but there were integrity failures."
        with open(log_file, "r") as lf:
            logged_failures = [line.strip() for line in lf.readlines() if line.strip()]

        for failure in expected_failures:
            assert failure in logged_failures, f"Corrupt artifact {failure} was not logged in {log_file}."

        assert len(logged_failures) == len(expected_failures), f"Log file contains unexpected entries. Expected {len(expected_failures)}, found {len(logged_failures)}."
    else:
        if os.path.exists(log_file):
            with open(log_file, "r") as lf:
                content = lf.read().strip()
            assert not content, f"Log file {log_file} should be empty, but contains data."