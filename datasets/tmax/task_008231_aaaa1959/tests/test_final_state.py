# test_final_state.py
import os
import tarfile
import tempfile
import pytest

FINAL_ARCHIVE = "/home/user/final_archive.tar.gz"

def test_final_archive_exists():
    assert os.path.isfile(FINAL_ARCHIVE), f"Final archive {FINAL_ARCHIVE} does not exist."
    assert tarfile.is_tarfile(FINAL_ARCHIVE), f"{FINAL_ARCHIVE} is not a valid tar file."

def test_final_archive_contents():
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(FINAL_ARCHIVE, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        release_dir = os.path.join(tmpdir, "release")
        assert os.path.isdir(release_dir), "The archive must contain a 'release' directory at its root."

        # Check api.bin
        api_bin_path = os.path.join(release_dir, "api.bin")
        assert os.path.isfile(api_bin_path), "'api.bin' is missing in the release directory."
        with open(api_bin_path, "rb") as f:
            api_content = f.read()
        assert api_content == b'\x05\x06\x07', "The 'api.bin' file does not contain the expected bytes from v2.0-draft."

        # Check README.md
        readme_path = os.path.join(release_dir, "README.md")
        assert os.path.isfile(readme_path), "'README.md' is missing in the release directory."
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read().strip()
        expected_readme = "Version 1.1 docs\nCONFIDENTIAL - DRAFT STATUS"
        assert readme_content == expected_readme, "The 'README.md' file does not contain the expected updated text."

        # Check symlink
        symlink_path = os.path.join(release_dir, "latest_api")
        # Note: os.path.islink might fail if we extracted without preserving symlinks, 
        # but tarfile.extractall does preserve symlinks on Unix.
        assert os.path.islink(symlink_path), "'latest_api' is not a symbolic link."

        link_target = os.readlink(symlink_path)
        assert link_target == "api.bin", f"'latest_api' should point to 'api.bin', but points to '{link_target}'."

def test_intermediate_directories():
    # Optional check based on task description
    assert os.path.isdir("/home/user/docs_processed"), "The docs_processed directory was not created."
    assert os.path.isdir("/home/user/release"), "The release directory was not created."