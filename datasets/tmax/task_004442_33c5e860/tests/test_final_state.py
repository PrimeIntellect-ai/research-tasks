# test_final_state.py

import os
import tarfile
import pytest

def test_update_archive_exists_and_size():
    archive_path = "/home/user/update.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    size = os.path.getsize(archive_path)
    threshold = 25000

    assert size <= threshold, (
        f"Archive size is {size} bytes, which exceeds the strict threshold of {threshold} bytes. "
        "Did you find and use the undocumented flag for the patch_gen binary to optimize patch sizes?"
    )

def test_update_archive_is_valid_and_contains_manifest():
    archive_path = "/home/user/update.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

        # Check if manifest is in the archive
        manifest_found = any(name.endswith("patch_manifest.txt") for name in names)
        assert manifest_found, "patch_manifest.txt not found in the archive."

        # Check if there are multiple files (patches + manifest)
        assert len(names) > 1, "The archive should contain patch files along with the manifest."