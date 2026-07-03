# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_final_archive_exists():
    assert os.path.isfile('/home/user/final_docs.tar.gz'), "/home/user/final_docs.tar.gz does not exist"

def test_c_source_code_atomic_rename():
    c_file = '/home/user/flattener.c'
    assert os.path.isfile(c_file), f"{c_file} does not exist"
    with open(c_file, 'r') as f:
        content = f.read()
    assert 'rename(' in content, "The C program does not seem to use rename() for atomic writes"

def test_archive_contents():
    archive_path = '/home/user/final_docs.tar.gz'
    assert os.path.isfile(archive_path), "Archive missing"

    expected_files = {
        '001_intro.md',
        '005_setup.md',
        '001_start_here.md',
        'legacy.md'
    }
    unexpected_files = {
        'loop1.md', 'loop2.md', 'loop3.md', 'broken_link.md',
        'missing.md'
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=tmpdir)

        extracted_files = set(os.listdir(tmpdir))

        # Check expected files are present
        for ef in expected_files:
            assert ef in extracted_files, f"Expected file {ef} is missing from the archive"

        # Check unexpected files are absent
        for uf in unexpected_files:
            assert uf not in extracted_files, f"Unexpected loop/broken file {uf} was found in the archive"

        # Check content modifications
        for filename in expected_files:
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, 'r') as f:
                lines = f.read().splitlines()
            assert len(lines) > 0, f"File {filename} is empty"
            assert lines[-1] == "ARCHIVED_2024_TECH_WRITER", f"File {filename} does not end with ARCHIVED_2024_TECH_WRITER"