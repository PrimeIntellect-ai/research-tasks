# test_final_state.py

import os
import tarfile
import struct
import tempfile
import pytest

CURATED_ARCHIVE = "/home/user/curated_artifacts.tar.gz"

def test_curated_archive_exists():
    assert os.path.exists(CURATED_ARCHIVE), f"Archive not found: {CURATED_ARCHIVE}"
    assert os.path.isfile(CURATED_ARCHIVE), f"Path is not a file: {CURATED_ARCHIVE}"
    assert tarfile.is_tarfile(CURATED_ARCHIVE), f"File is not a valid tar archive: {CURATED_ARCHIVE}"

def test_curated_archive_contents():
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(CURATED_ARCHIVE, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        log_path = os.path.join(tmpdir, "artifact_registry.log")
        bin_dir = os.path.join(tmpdir, "bin")

        assert os.path.exists(log_path), "artifact_registry.log is missing from the archive root."
        assert os.path.exists(bin_dir) and os.path.isdir(bin_dir), "bin/ directory is missing from the archive root."

        with open(log_path, "r") as f:
            lines = f.read().strip().split("\n")

        # Each record is 5 lines
        assert len(lines) % 5 == 0, "Log file does not have a multiple of 5 lines, indicating malformed records."
        num_records = len(lines) // 5

        # Based on random seed 42, exactly 47 records should be valid
        assert num_records == 47, f"Expected 47 valid records, found {num_records}."

        log_files = set()

        for i in range(num_records):
            record = lines[i*5 : (i+1)*5]
            assert record[0] == "[Record Start]", f"Record {i} does not start with [Record Start]"
            assert record[1].startswith("Artifact ID: ")
            assert record[2].startswith("File: ")
            assert record[3].startswith("Expected Magic: ")
            assert record[4] == "Status: VERIFIED", f"Record {i} status is not VERIFIED. Found: {record[4]}"

            file_rel_path = record[2].split("File: ")[1].strip()
            log_files.add(file_rel_path)

            expected_magic_str = record[3].split("Expected Magic: ")[1].strip()
            expected_magic = int(expected_magic_str, 16)

            # Check file exists and magic matches
            extracted_file_path = os.path.join(tmpdir, file_rel_path)
            assert os.path.exists(extracted_file_path), f"File {file_rel_path} listed in log but missing from archive."

            with open(extracted_file_path, "rb") as bf:
                magic_bytes = bf.read(4)
                assert len(magic_bytes) == 4, f"File {file_rel_path} is too short."
                actual_magic = struct.unpack(">I", magic_bytes)[0]
                assert actual_magic == expected_magic, f"Magic mismatch in {file_rel_path}. Expected {expected_magic_str}, got 0x{actual_magic:08X}"

        # Check that bin/ directory contains ONLY the files listed in the log
        actual_files = set()
        for root, _, files in os.walk(bin_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, tmpdir)
                actual_files.add(rel_path)

        assert actual_files == log_files, f"Files in bin/ do not match log exactly. Difference: {actual_files.symmetric_difference(log_files)}"