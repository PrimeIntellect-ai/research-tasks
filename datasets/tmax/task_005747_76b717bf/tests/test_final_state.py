# test_final_state.py

import os
import tarfile

def test_incremental_archive_exists():
    archive_path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

def test_incremental_archive_contents():
    archive_path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Check that there are exactly 2 files
        files = [m for m in members if m.isfile()]
        assert len(files) == 2, f"Expected exactly 2 files in the archive, found {len(files)}."

        # Check that there are no directory paths (just filenames)
        for f in files:
            assert "/" not in f.name, f"File '{f.name}' in archive contains directory paths, but should be at the root."

        names = [f.name for f in files]
        assert "Reference_API_v1.md" in names, "Reference_API_v1.md is missing from the archive."
        assert "Reference_API_v2.md" in names, "Reference_API_v2.md is missing from the archive."

        # Verify contents
        with tar.extractfile("Reference_API_v1.md") as f1:
            content1 = f1.read().decode("utf-8")
            assert "API V1 Content - UPDATED" in content1, "Content of Reference_API_v1.md is incorrect."

        with tar.extractfile("Reference_API_v2.md") as f2:
            content2 = f2.read().decode("utf-8")
            assert "API V2 Content" in content2, "Content of Reference_API_v2.md is incorrect."