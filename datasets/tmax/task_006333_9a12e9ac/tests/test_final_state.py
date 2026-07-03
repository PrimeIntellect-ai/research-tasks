# test_final_state.py

import os
import tarfile
import hashlib
import tempfile
import pytest

SCRIPT_PATH = "/home/user/archive_logs.py"
ARCHIVE_PATH = "/home/user/backups/logs_archive.tar.gz"
SOURCE_DIR = "/home/user/logs_source"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Python script not found at {SCRIPT_PATH}"

def test_archive_exists():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive not found at {ARCHIVE_PATH}"

def test_archive_contents_and_manifest():
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive"

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getnames()

        expected_files = {
            "db_20231001.log",
            "web_20231002.log",
            "app_20231004.log",
            "manifest.sha256"
        }

        actual_files = set(members)
        assert expected_files.issubset(actual_files), f"Archive is missing expected files. Expected {expected_files}, got {actual_files}"
        assert "api_20231003.log" not in actual_files, "api.log should not be included as it is <= 10KB"

        # Verify no directories are included (files should be at root)
        for member in tar.getmembers():
            assert not member.isdir(), f"Archive contains directory {member.name}, but files should be at the root."
            assert "/" not in member.name, f"Archive contains nested file {member.name}, but files should be at the root."

        with tempfile.TemporaryDirectory() as tmpdir:
            tar.extractall(path=tmpdir)

            # Verify manifest
            manifest_path = os.path.join(tmpdir, "manifest.sha256")
            assert os.path.isfile(manifest_path), "manifest.sha256 was not extracted correctly"

            with open(manifest_path, "r") as f:
                manifest_lines = f.read().strip().split('\n')

            assert len(manifest_lines) == 3, f"manifest.sha256 should have exactly 3 lines, found {len(manifest_lines)}"

            manifest_data = {}
            for line in manifest_lines:
                parts = line.split("  ")
                assert len(parts) == 2, f"Invalid manifest line format: '{line}'. Expected '<hash>  <filename>'"
                file_hash, filename = parts
                manifest_data[filename] = file_hash

            expected_log_files = ["db_20231001.log", "web_20231002.log", "app_20231004.log"]
            for log_file in expected_log_files:
                assert log_file in manifest_data, f"{log_file} missing from manifest.sha256"

                # Calculate actual hash
                extracted_log_path = os.path.join(tmpdir, log_file)
                assert os.path.isfile(extracted_log_path), f"Expected {log_file} to be extracted"

                with open(extracted_log_path, "rb") as f:
                    actual_hash = hashlib.sha256(f.read()).hexdigest()

                assert manifest_data[log_file] == actual_hash, f"Hash mismatch in manifest for {log_file}"

                # Also verify the content matches the original source file
                original_filename = log_file.split("_")[0] + ".log"
                original_filepath = os.path.join(SOURCE_DIR, original_filename)

                with open(original_filepath, "rb") as f:
                    original_hash = hashlib.sha256(f.read()).hexdigest()

                assert actual_hash == original_hash, f"Content of {log_file} in archive does not match original {original_filename}"