# test_final_state.py

import os
import subprocess
import pytest

def test_final_archive_exists_and_size():
    archive_path = "/home/user/processed/final_archive.tar.xz"
    assert os.path.exists(archive_path), f"The file {archive_path} does not exist."
    assert os.path.isfile(archive_path), f"The path {archive_path} is not a file."

    size = os.path.getsize(archive_path)
    assert size <= 25000, f"Archive size is {size} bytes, which exceeds the threshold of 25000 bytes. The bloat was not properly removed or compression was insufficient."

def test_final_archive_contents():
    archive_path = "/home/user/processed/final_archive.tar.xz"
    assert os.path.exists(archive_path), f"The file {archive_path} does not exist."

    extract_dir = "/tmp/verifier_extract"
    os.makedirs(extract_dir, exist_ok=True)

    # Extract the archive
    result = subprocess.run(["tar", "-xf", archive_path, "-C", extract_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to extract {archive_path}. Is it a valid tar.xz archive? Error: {result.stderr}"

    csv_path = os.path.join(extract_dir, "summary.csv")
    assert os.path.exists(csv_path), f"summary.csv was not found inside the extracted archive."

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 5001, f"Expected exactly 5001 lines in summary.csv (5000 records + 1 header), but got {len(lines)}."
    assert lines[0].strip() == "Time,Level,Error", f"Expected header 'Time,Level,Error', but got '{lines[0].strip()}'."