# test_final_state.py

import os
import tarfile
import pytest

def test_extracted_data_dir():
    """Verify that the extracted_data directory exists."""
    extracted_dir = "/home/user/extracted_data"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

def test_merged_large_data_file():
    """Verify the merged_large_data.txt file exists and has the correct number of lines."""
    merged_file = "/home/user/merged_large_data.txt"
    assert os.path.isfile(merged_file), f"File {merged_file} does not exist."

    with open(merged_file, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 2000, f"Expected 2000 lines in {merged_file}, but found {len(lines)}."

def test_split_data_chunks():
    """Verify the split_data directory contains the correct chunks with 500 lines each."""
    split_dir = "/home/user/split_data"
    assert os.path.isdir(split_dir), f"Directory {split_dir} does not exist."

    expected_files = ["chunk_aa.txt", "chunk_ab.txt", "chunk_ac.txt", "chunk_ad.txt"]
    files_in_dir = os.listdir(split_dir)

    for expected_file in expected_files:
        assert expected_file in files_in_dir, f"Expected file {expected_file} is missing in {split_dir}."

        filepath = os.path.join(split_dir, expected_file)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        assert len(lines) == 500, f"Expected 500 lines in {expected_file}, but found {len(lines)}."

    # Check that there are no extra files in the split_data directory
    txt_files = [f for f in files_in_dir if f.endswith('.txt')]
    assert len(txt_files) == 4, f"Expected exactly 4 .txt chunk files, but found {len(txt_files)}."

def test_final_backup_archive():
    """Verify the final_backup.tar.gz exists and contains the split_data directory and chunks."""
    archive_path = "/home/user/final_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()

        # Check if any path in the archive contains 'split_data'
        split_data_present = any("split_data" in name for name in names)
        assert split_data_present, "The split_data directory is missing from the final backup archive."

        # Check for chunk files in the archive
        expected_chunks = ["chunk_aa.txt", "chunk_ab.txt", "chunk_ac.txt", "chunk_ad.txt"]
        for chunk in expected_chunks:
            chunk_present = any(name.endswith(chunk) for name in names)
            assert chunk_present, f"Chunk {chunk} is missing from the final backup archive."