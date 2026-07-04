# test_final_state.py

import os
import tarfile
import pytest

def test_c_program_exists():
    c_source = "/home/user/processor.c"
    binary = "/home/user/processor"

    assert os.path.isfile(c_source), f"C source file {c_source} is missing."
    assert os.path.isfile(binary), f"Compiled binary {binary} is missing."
    assert os.access(binary, os.X_OK), f"Binary {binary} is not executable."

def test_processed_files_exist_and_content():
    processed_dir = "/home/user/processed_docs"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} is missing."

    expected_files = {
        "user_manual.txt_part1.txt": "Welcome to the QuantumFlow User Manual.\nThis system is the best QuantumFlow has to offer.",
        "user_manual.txt_part2.txt": "Chapter 2: Operation\nTo operate QuantumFlow, press the big red button.",
        "user_manual.txt_part3.txt": "Chapter 3: Maintenance\nQuantumFlow requires daily oiling.",
        "api_guide.txt_part1.txt": "QuantumFlow API Documentation",
        "api_guide.txt_part2.txt": "Endpoints:\nGET /api/legacy\nReturns QuantumFlow status."
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(processed_dir, filename)
        assert os.path.isfile(filepath), f"Expected processed file {filepath} is missing."

        with open(filepath, "r") as f:
            content = f.read().strip()

        assert content == expected_content, f"Content mismatch in {filepath}. Expected:\n{expected_content}\nGot:\n{content}"

def test_draft_notes_not_processed():
    processed_dir = "/home/user/processed_docs"
    if os.path.isdir(processed_dir):
        for filename in os.listdir(processed_dir):
            assert "draft_notes" not in filename, f"Draft notes should not have been processed, found {filename}."

def test_tar_archive():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    expected_filenames = [
        "user_manual.txt_part1.txt",
        "user_manual.txt_part2.txt",
        "user_manual.txt_part3.txt",
        "api_guide.txt_part1.txt",
        "api_guide.txt_part2.txt"
    ]

    with tarfile.open(archive_path, "r:gz") as tar:
        tar_members = tar.getnames()

        # Check that all expected files are in the archive
        for expected in expected_filenames:
            found = any(expected in member for member in tar_members)
            assert found, f"Expected file {expected} not found in archive {archive_path}."

        # Check that no draft notes are in the archive
        for member in tar_members:
            assert "draft_notes" not in member, f"Draft notes found in archive {archive_path}."