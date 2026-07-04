# test_final_state.py

import os
import subprocess
import tarfile

def test_corrupted_archives_log():
    """Check that corrupted_archives.log contains exactly corrupt_data.zip"""
    log_path = "/home/user/corrupted_archives.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 line in log, found {len(lines)}."
    assert lines[0] == "corrupt_data.zip", f"Expected 'corrupt_data.zip' in log, got '{lines[0]}'."

def test_extracted_data_contents():
    """Check that valid data was extracted correctly."""
    valid_data1_dir = "/home/user/extracted/valid_data1"
    valid_data2_dir = "/home/user/extracted/valid_data2"

    assert os.path.isdir(valid_data1_dir), f"{valid_data1_dir} does not exist."
    assert os.path.isdir(valid_data2_dir), f"{valid_data2_dir} does not exist."

    assert os.path.isfile(os.path.join(valid_data1_dir, "info.txt")), "valid_data1/info.txt missing"
    assert os.path.isfile(os.path.join(valid_data1_dir, "shared_measurements.txt")), "valid_data1/shared_measurements.txt missing"

    assert os.path.isfile(os.path.join(valid_data2_dir, "info.txt")), "valid_data2/info.txt missing"
    assert os.path.isfile(os.path.join(valid_data2_dir, "shared_measurements_copy.txt")), "valid_data2/shared_measurements_copy.txt missing"

def test_broken_link_removal():
    """Check that the broken symlink was removed."""
    broken_link_path = "/home/user/extracted/valid_data2/broken_link.txt"
    assert not os.path.exists(broken_link_path) and not os.path.islink(broken_link_path), \
        f"Broken link {broken_link_path} should have been removed."

def test_hard_link_deduplication():
    """Check that identical files were hard-linked."""
    file1 = "/home/user/extracted/valid_data1/shared_measurements.txt"
    file2 = "/home/user/extracted/valid_data2/shared_measurements_copy.txt"

    assert os.path.isfile(file1), f"{file1} does not exist."
    assert os.path.isfile(file2), f"{file2} does not exist."

    stat1 = os.stat(file1)
    stat2 = os.stat(file2)

    assert stat1.st_ino == stat2.st_ino, f"Files {file1} and {file2} do not share the same inode. Deduplication failed."

def test_final_archive():
    """Check that the final archive exists, is a valid bz2 tarball, and preserves hard links."""
    archive_path = "/home/user/clean_dataset.tar.bz2"
    assert os.path.isfile(archive_path), f"Final archive {archive_path} does not exist."

    # Check if it's a valid bzip2 tarball
    try:
        with tarfile.open(archive_path, "r:bz2") as tar:
            members = tar.getmembers()

            # Check for hard links in the archive
            has_hardlink = any(m.islnk() for m in members)
            assert has_hardlink, "No hard links found in the archive. Hard links were not preserved."

            # Verify contents
            names = [m.name for m in members]
            # The archive should contain the extracted files
            # Depending on how it was archived, paths might vary slightly, but basenames should be present
            basenames = [os.path.basename(name) for name in names]
            assert "info.txt" in basenames, "info.txt missing from final archive."
            assert "shared_measurements.txt" in basenames or "shared_measurements_copy.txt" in basenames, \
                "Shared measurements file missing from final archive."
    except tarfile.ReadError:
        assert False, f"{archive_path} is not a valid bzip2 compressed tarball."