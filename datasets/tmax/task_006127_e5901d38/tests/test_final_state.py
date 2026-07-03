# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_final_dataset_archive_exists():
    """Verify that the final dataset archive exists."""
    archive_path = "/home/user/final_dataset.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

def test_final_dataset_contents():
    """Verify the contents of the final dataset archive."""
    archive_path = "/home/user/final_dataset.tar.gz"
    if not os.path.isfile(archive_path):
        pytest.fail(f"Archive {archive_path} does not exist, cannot check contents.")

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract {archive_path}: {e}")

        # Find all files in the extracted directory
        extracted_files = []
        for root, _, files in os.walk(tmpdir):
            for file in files:
                extracted_files.append(os.path.join(root, file))

        # Expected file names
        expected_names = [
            "dataset_chunk_000.txt",
            "dataset_chunk_001.txt",
            "dataset_chunk_002.txt"
        ]

        found_files = {name: None for name in expected_names}

        for filepath in extracted_files:
            basename = os.path.basename(filepath)
            if basename in found_files:
                found_files[basename] = filepath
            else:
                # We can ignore other files like directories or hidden files, 
                # but let's ensure the main chunks are present.
                pass

        for name in expected_names:
            assert found_files[name] is not None, f"Expected file {name} not found in the archive."

        # Check line counts and contents
        expected_line_counts = {
            "dataset_chunk_000.txt": 500,
            "dataset_chunk_001.txt": 500,
            "dataset_chunk_002.txt": 250
        }

        total_lines = 0
        for name, filepath in found_files.items():
            if filepath is None:
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            assert len(lines) == expected_line_counts[name], \
                f"File {name} has {len(lines)} lines, expected {expected_line_counts[name]}."

            for i, line in enumerate(lines):
                assert "DATA: " not in line, f"Found 'DATA: ' in {name} at line {i+1}."
                assert "CORRUPT" not in line, f"Found 'CORRUPT' in {name} at line {i+1}."
                total_lines += 1

        assert total_lines == 1250, f"Total valid lines across all chunks is {total_lines}, expected 1250."