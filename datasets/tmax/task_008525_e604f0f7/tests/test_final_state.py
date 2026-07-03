# test_final_state.py
import os
import tarfile
import zipfile
import pytest

def test_summary_txt():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 2, f"Expected exactly 2 lines in summary.txt, found {len(content)}."
    assert content[0] == "VALID_ELF_COUNT=3", f"Expected VALID_ELF_COUNT=3, got {content[0]}."
    assert content[1] == "LOG_CHUNK_COUNT=8", f"Expected LOG_CHUNK_COUNT=8, got {content[1]}."

def test_elf_archive_contents():
    archive_path = "/home/user/elf_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Ensure no directories are in the archive
        for member in members:
            assert member.isfile(), f"Archive contains non-file element: {member.name}. Directory structure should not be included."
            assert "/" not in member.name, f"Archive contains nested paths: {member.name}. Only flat files should be included."

        filenames = sorted([m.name for m in members])
        expected_files = sorted(["binary1_ls", "binary2_cat", "binary3_echo.elf"])

        assert filenames == expected_files, f"Archive contains incorrect files. Expected {expected_files}, got {filenames}."

def test_logs_archive_contents():
    archive_path = "/home/user/logs_archive.zip"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert zipfile.is_zipfile(archive_path), f"File {archive_path} is not a valid zip archive."

    expected_chunks = sorted([
        "system_run.log_chunk_aa", "system_run.log_chunk_ab", "system_run.log_chunk_ac",
        "error_dump.log_chunk_aa",
        "access.log_chunk_aa", "access.log_chunk_ab", "access.log_chunk_ac", "access.log_chunk_ad"
    ])

    with zipfile.ZipFile(archive_path, "r") as zf:
        infolist = zf.infolist()

        for info in infolist:
            assert not info.is_dir(), f"Archive contains directory: {info.filename}. Directory structure should not be included."
            assert "/" not in info.filename, f"Archive contains nested paths: {info.filename}. Only flat files should be included."

        filenames = sorted([info.filename for info in infolist])
        assert filenames == expected_chunks, f"Archive contains incorrect chunk files. Expected {expected_chunks}, got {filenames}."