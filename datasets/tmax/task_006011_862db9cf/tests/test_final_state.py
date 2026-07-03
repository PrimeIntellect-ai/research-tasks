# test_final_state.py

import os
import struct
import zlib
import pytest

def test_executables_and_scripts_exist():
    """Verify that the required source, executable, script, and stamp files exist."""
    assert os.path.exists("/home/user/compress_append.c"), "C source file compress_append.c is missing."
    assert os.path.exists("/home/user/compress_append"), "Compiled executable compress_append is missing."
    assert os.access("/home/user/compress_append", os.X_OK), "compress_append is not executable."

    assert os.path.exists("/home/user/backup.sh"), "Bash script backup.sh is missing."
    assert os.path.exists("/home/user/backup.stamp"), "State file backup.stamp is missing."

def test_archive_exists():
    """Verify that the master archive was created."""
    assert os.path.exists("/home/user/master_archive.dat"), "Archive file master_archive.dat is missing."

def test_archive_contents():
    """Parse the custom binary archive and verify the incremental backup logic."""
    archive_path = "/home/user/master_archive.dat"
    assert os.path.exists(archive_path), "Archive file master_archive.dat is missing."

    records = []
    with open(archive_path, "rb") as f:
        while True:
            len_byte = f.read(1)
            if not len_byte:
                break

            assert len(len_byte) == 1, "Unexpected EOF while reading filename length."
            name_len = struct.unpack("B", len_byte)[0]

            filename_bytes = f.read(name_len)
            assert len(filename_bytes) == name_len, "Unexpected EOF while reading filename."
            filename = filename_bytes.decode("utf-8")

            size_bytes = f.read(4)
            assert len(size_bytes) == 4, "Unexpected EOF while reading compressed payload size."
            comp_size = struct.unpack("<I", size_bytes)[0]

            comp_data = f.read(comp_size)
            assert len(comp_data) == comp_size, "Unexpected EOF while reading compressed data."

            try:
                uncompressed = zlib.decompress(comp_data).decode("utf-8")
            except Exception as e:
                pytest.fail(f"Failed to decompress payload for {filename}: {e}")

            records.append((filename, uncompressed))

    assert len(records) == 4, f"Expected exactly 4 backup records, found {len(records)}."

    first_run = sorted(records[:3], key=lambda x: x[0])

    expected_first_run = [
        ("alpha.txt", "Initial content for alpha file. This needs to be backed up.\n"),
        ("beta.txt", "Beta file is somewhat shorter.\n"),
        ("gamma.txt", "Gamma file is the third file in this directory.\n")
    ]

    for i in range(3):
        assert first_run[i][0] == expected_first_run[i][0], f"Expected {expected_first_run[i][0]} in first run, got {first_run[i][0]}"
        assert first_run[i][1] == expected_first_run[i][1], f"Content mismatch for {first_run[i][0]} in first run."

    assert records[3][0] == "alpha.txt", "The fourth record (incremental backup) should be alpha.txt."

    expected_mod = "Initial content for alpha file. This needs to be backed up.\n[MODIFIED] Additional data appended.\n"
    assert records[3][1] == expected_mod, "Content mismatch for the modified alpha.txt in the incremental backup."