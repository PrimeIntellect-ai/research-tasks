# test_final_state.py
import os
import pytest

def test_archive_size_metric():
    target_file = "/home/user/archive.zst"

    assert os.path.exists(target_file), f"The target output file {target_file} does not exist."
    assert os.path.isfile(target_file), f"The target {target_file} is not a file."

    size = os.path.getsize(target_file)

    assert size <= 3000, f"Metric failed: file size {size} bytes exceeds the maximum threshold of 3000 bytes. Compression level too low, debug lines not stripped, or 2022 files included."
    assert size >= 100, f"Metric failed: file size {size} bytes is below the minimum threshold of 100 bytes. File is suspiciously small, likely empty or invalid data."

def test_pyzstd_bad_flag_removed():
    setup_path = "/app/pyzstd-0.15.9/setup.py"
    if os.path.exists(setup_path):
        with open(setup_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        assert "-fbreak-my-build-123" not in content, "The bad compiler flag '-fbreak-my-build-123' was not removed from setup.py."