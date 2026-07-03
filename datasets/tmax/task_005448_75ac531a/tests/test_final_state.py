# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_incremental_archive_exists():
    archive_path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(archive_path), f"The incremental archive was not found at {archive_path}"

def test_incremental_archive_contents():
    archive_path = "/home/user/incremental.tar.gz"
    assert tarfile.is_tarfile(archive_path), f"The file at {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Ensure files are not nested in directories
        filenames = [m.name for m in members if m.isfile()]

        # Check expected files
        assert "app.conf" in filenames, "app.conf is missing from the incremental archive."
        assert "cache.conf" in filenames, "cache.conf is missing from the incremental archive."

        # Check unexpected files
        assert "db.conf" not in filenames, "db.conf should not be in the incremental archive (it was unchanged)."
        assert "log.conf" not in filenames, "log.conf should not be in the incremental archive (it was unchanged)."

        # Check that there are exactly 2 files
        assert len(filenames) == 2, f"Expected exactly 2 files in the archive, but found {len(filenames)}: {filenames}"

        # Verify contents
        app_conf_member = tar.getmember("app.conf")
        app_conf_f = tar.extractfile(app_conf_member)
        assert app_conf_f is not None, "Failed to extract app.conf"
        app_content = app_conf_f.read().decode("utf-8")
        assert app_content == "theme=light\n", f"Incorrect content in app.conf. Expected 'theme=light\\n', got {app_content!r}"

        cache_conf_member = tar.getmember("cache.conf")
        cache_conf_f = tar.extractfile(cache_conf_member)
        assert cache_conf_f is not None, "Failed to extract cache.conf"
        cache_content = cache_conf_f.read().decode("utf-8")
        assert cache_content == "size=1024\n", f"Incorrect content in cache.conf. Expected 'size=1024\\n', got {cache_content!r}"