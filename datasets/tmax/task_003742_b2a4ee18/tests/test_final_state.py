# test_final_state.py

import os
import stat
import hashlib
import pytest

OUTPUT_CSV = "/home/user/output.csv"
TEST_SCRIPT = "/home/user/test_reproducibility.sh"
LOG_FILE = "/home/user/reproducibility_log.txt"

def test_output_csv_content():
    assert os.path.isfile(OUTPUT_CSV), f"{OUTPUT_CSV} is missing."

    with open(OUTPUT_CSV, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "sample_id,out1,out2,out3",
        "S1,1.5,0.5,1.0",
        "S2,6.0,4.0,5.0",
        "S3,18.0,14.0,16.0"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {OUTPUT_CSV}, got {len(lines)}."
    for idx, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {idx + 1} in {OUTPUT_CSV} does not match expected output. Expected '{expected}', got '{actual}'."

def test_reproducibility_script_exists_and_executable():
    assert os.path.isfile(TEST_SCRIPT), f"{TEST_SCRIPT} is missing."
    st = os.stat(TEST_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{TEST_SCRIPT} is not executable."

def test_reproducibility_log():
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} is missing."

    with open(LOG_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {LOG_FILE}, got {len(lines)}."

    # Calculate md5 of output.csv
    with open(OUTPUT_CSV, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    for idx, line in enumerate(lines):
        parts = line.split()
        assert len(parts) >= 2, f"Line {idx + 1} in {LOG_FILE} is not a valid md5sum output."
        assert parts[0] == file_hash, f"Hash on line {idx + 1} in {LOG_FILE} does not match the actual MD5 hash of {OUTPUT_CSV}."
        assert "output.csv" in parts[1], f"Filename on line {idx + 1} in {LOG_FILE} does not reference output.csv."