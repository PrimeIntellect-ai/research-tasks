# test_final_state.py

import os
import tarfile
import pytest

ARCHIVE_PATH = '/home/user/curated_archive.tar.gz'

def test_archive_exists():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive not found at expected path: {ARCHIVE_PATH}"
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File at {ARCHIVE_PATH} is not a valid tar archive."

def test_archive_contents():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive not found: {ARCHIVE_PATH}"

    with tarfile.open(ARCHIVE_PATH, 'r:gz') as tar:
        names = tar.getnames()

        # Helper to check if a file path is in the tar
        def contains_path(expected_path):
            return any(name == expected_path or name.endswith('/' + expected_path) for name in names)

        # EXP-001 should be included
        assert contains_path('EXP-001/exp1.log'), "EXP-001/exp1.log is missing from the archive."
        assert contains_path('EXP-001/data1.bin'), "EXP-001/data1.bin is missing from the archive."

        # EXP-003 should be included
        assert contains_path('EXP-003/exp3.log'), "EXP-003/exp3.log is missing from the archive."
        assert contains_path('EXP-003/data3.bin'), "EXP-003/data3.bin is missing from the archive."

        # EXP-002 should NOT be included
        for name in names:
            assert 'EXP-002' not in name, f"Failed experiment EXP-002 was found in the archive: {name}"

        # Absolute paths should NOT be included
        for name in names:
            assert not name.startswith('/home/user'), f"Absolute host path found in archive: {name}"
            assert not name.startswith('home/user'), f"Relative host path found in archive: {name}"

def test_archive_file_data():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive not found: {ARCHIVE_PATH}"

    with tarfile.open(ARCHIVE_PATH, 'r:gz') as tar:
        # Check data1.bin content
        try:
            member = tar.getmember('EXP-001/data1.bin')
            with tar.extractfile(member) as f:
                assert f.read() == b'\x00\x01\x02', "EXP-001/data1.bin content is incorrect."
        except KeyError:
            pytest.fail("EXP-001/data1.bin not found at the exact expected path inside the archive.")

        # Check data3.bin content
        try:
            member = tar.getmember('EXP-003/data3.bin')
            with tar.extractfile(member) as f:
                assert f.read() == b'\x06\x07\x08', "EXP-003/data3.bin content is incorrect."
        except KeyError:
            pytest.fail("EXP-003/data3.bin not found at the exact expected path inside the archive.")