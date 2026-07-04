# test_final_state.py

import os
import hashlib
import pytest

def test_extractor_files_exist():
    """Test that the C source and compiled extractor exist."""
    source_file = "/home/user/extractor.c"
    binary_file = "/home/user/extractor"

    assert os.path.isfile(source_file), f"Source file missing: {source_file}"
    assert os.path.isfile(binary_file), f"Compiled binary missing: {binary_file}"
    assert os.access(binary_file, os.X_OK), f"Extractor binary is not executable: {binary_file}"

def test_extracted_files_exist_and_correct():
    """Test that the artifacts were extracted correctly and contain the expected data."""
    extracted_dir = "/home/user/extracted_artifacts"
    assert os.path.isdir(extracted_dir), f"Extracted artifacts directory missing: {extracted_dir}"

    expected_files = {
        "init_sys.elf": b"ELF_mock_init_binary" * 50,
        "kernel_module.bin": b"mock_kernel_data_123" * 100,
        "tcp_handler.so": b"shared_object_tcp_stuff" * 80,
        "udp_handler.so": b"shared_object_udp_stuff" * 80
    }

    for fname, expected_content in expected_files.items():
        fpath = os.path.join(extracted_dir, fname)
        assert os.path.isfile(fpath), f"Extracted file missing: {fpath}"

        with open(fpath, "rb") as f:
            actual_content = f.read()

        assert actual_content == expected_content, f"Content mismatch for extracted file: {fname}"

def test_manifest_matches_expected():
    """Test that the generated manifest matches the expected manifest."""
    manifest_path = "/home/user/manifest.txt"
    expected_path = "/tmp/expected_manifest.txt"

    assert os.path.exists(manifest_path), f"Manifest file not found at {manifest_path}"
    assert os.path.exists(expected_path), f"Expected manifest not found at {expected_path}"

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    with open(expected_path, "r") as f:
        expected_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), "Manifest does not have the correct number of entries."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Manifest line {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"