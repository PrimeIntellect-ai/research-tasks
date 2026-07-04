# test_final_state.py

import os
import pytest

def test_incremental_pak_exists_and_size():
    file_path = '/home/user/incremental.pak'

    assert os.path.exists(file_path), f"The final archive file was not found at {file_path}. Did you run the legacy packer?"
    assert os.path.isfile(file_path), f"The path {file_path} exists but is not a file."

    size = os.path.getsize(file_path)
    threshold = 1500

    assert size <= threshold, (
        f"The file size of {file_path} is {size} bytes, which exceeds the maximum allowed threshold of {threshold} bytes. "
        "This indicates that either old files were not ignored, or non-ERROR/CRITICAL log entries were included in the staging files."
    )