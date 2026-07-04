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

def test_script_exists():
    script_path = "/home/user/filter_logs.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

def test_processed_logs_directory():
    processed_dir = "/home/user/processed_logs/"
    assert os.path.isdir(processed_dir), f"Processed logs directory not found at {processed_dir}"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = set(f for f in os.listdir(clean_dir) if f.endswith(".tar.gz"))
    evil_files = set(f for f in os.listdir(evil_dir) if f.endswith(".tar.gz"))

    processed_files = set(f for f in os.listdir(processed_dir) if f.endswith(".tar.gz"))

    # Check that all clean files are preserved
    missing_clean = clean_files - processed_files
    assert not missing_clean, f"{len(missing_clean)} of {len(clean_files)} clean logs modified or missing: {', '.join(list(missing_clean)[:5])}"

    # Check that no evil files bypassed the filter
    bypassed_evil = evil_files.intersection(processed_files)
    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil logs bypassed the filter: {', '.join(list(bypassed_evil)[:5])}"

    # Check that no unexpected files are present
    unexpected = processed_files - clean_files - evil_files
    assert not unexpected, f"Unexpected files found in processed_logs: {', '.join(list(unexpected)[:5])}"

    # Check that the preserved files are identical to the original clean files
    for f in clean_files:
        orig_path = os.path.join(clean_dir, f)
        proc_path = os.path.join(processed_dir, f)
        assert get_sha256(orig_path) == get_sha256(proc_path), f"File {f} was modified during processing"

def test_retention_manifest():
    manifest_path = "/home/user/retention_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file not found at {manifest_path}"

    clean_dir = "/app/corpus/clean/"
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".tar.gz")]

    expected_manifest = {}
    for f in clean_files:
        expected_manifest[f] = get_sha256(os.path.join(clean_dir, f))

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(clean_files), f"Manifest should contain exactly {len(clean_files)} lines, found {len(lines)}"

    parsed_manifest = {}
    for line in lines:
        parts = line.split()
        assert len(parts) >= 2, f"Invalid manifest line format: {line}"
        checksum = parts[0]
        filename = parts[1]
        # Handle cases where filename might have a path or just the basename
        basename = os.path.basename(filename)
        parsed_manifest[basename] = checksum

    missing_in_manifest = set(expected_manifest.keys()) - set(parsed_manifest.keys())
    assert not missing_in_manifest, f"Files missing from manifest: {', '.join(list(missing_in_manifest)[:5])}"

    for basename, expected_checksum in expected_manifest.items():
        actual_checksum = parsed_manifest.get(basename)
        assert actual_checksum == expected_checksum, f"Checksum mismatch for {basename}: expected {expected_checksum}, got {actual_checksum}"