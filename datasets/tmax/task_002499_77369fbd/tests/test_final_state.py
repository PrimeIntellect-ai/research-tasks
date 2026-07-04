# test_final_state.py

import os
import tarfile
import pytest

def test_final_archive_exists_and_size():
    file_path = "/home/user/optimized_pool.tar.xz"
    assert os.path.exists(file_path), f"Archive not found at {file_path}"

    size_bytes = os.path.getsize(file_path)
    threshold = 1250000
    assert size_bytes <= threshold, f"Archive size {size_bytes} bytes exceeds the maximum allowed threshold of {threshold} bytes."

def test_storage_pool_cleaned_up():
    pool_dir = "/home/user/storage_pool"
    if os.path.exists(pool_dir):
        # The prompt states: "Remove all original and intermediate files in /home/user/storage_pool/"
        # We check for the specific initial files and common extraction directories to ensure cleanup.
        initial_files = ["wrapper.zip", "copy2.zip", "copy3.zip", "encrypted_logs.zip", "nested.tar.gz"]
        for f in initial_files:
            file_path = os.path.join(pool_dir, f)
            assert not os.path.exists(file_path), f"Original/intermediate file {f} was not removed from {pool_dir}."

        intermediate_dirs = ["raw_data", "dupes"]
        for d in intermediate_dirs:
            dir_path = os.path.join(pool_dir, d)
            assert not os.path.exists(dir_path), f"Intermediate directory {d} was not removed from {pool_dir}."

def test_archive_validity():
    file_path = "/home/user/optimized_pool.tar.xz"
    if not os.path.exists(file_path):
        pytest.skip("Archive does not exist, skipping validity check.")

    try:
        with tarfile.open(file_path, "r:xz") as tar:
            members = tar.getmembers()
            # Ensure the archive actually contains files and isn't just an empty tarball
            files = [m for m in members if m.isfile()]
            assert len(files) > 0, "The final archive is empty. It must contain the deduplicated files."
    except tarfile.ReadError:
        pytest.fail(f"The file at {file_path} is not a valid tar.xz archive.")
    except Exception as e:
        pytest.fail(f"Failed to read the archive at {file_path}: {e}")