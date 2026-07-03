# test_final_state.py
import os
import struct
import gzip
import pytest

ARCHIVE_PATH = "/home/user/incremental.archive"
RAW_LOGS_DIR = "/home/user/raw_logs"
LAST_RUN_FILE = "/home/user/last_run.txt"

def get_expected_data():
    if not os.path.exists(LAST_RUN_FILE):
        pytest.fail(f"Missing {LAST_RUN_FILE}")

    with open(LAST_RUN_FILE, "r") as f:
        try:
            last_run_time = int(f.read().strip())
        except ValueError:
            pytest.fail(f"Invalid timestamp in {LAST_RUN_FILE}")

    if not os.path.exists(RAW_LOGS_DIR):
        pytest.fail(f"Missing {RAW_LOGS_DIR}")

    expected_data = {}
    for filename in os.listdir(RAW_LOGS_DIR):
        if not filename.endswith(".log"):
            continue

        filepath = os.path.join(RAW_LOGS_DIR, filename)
        mtime = os.stat(filepath).st_mtime

        if mtime > last_run_time:
            with open(filepath, "r") as f:
                lines = f.readlines()

            critical_lines = [line for line in lines if "CRITICAL" in line]
            if critical_lines:
                expected_data[filename] = "".join(critical_lines).encode("utf-8")
            else:
                expected_data[filename] = b""

    return expected_data

def test_archive_exists():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."

def test_archive_contents():
    expected_data = get_expected_data()

    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."

    found_files = set()

    with open(ARCHIVE_PATH, "rb") as f:
        while True:
            len_bytes = f.read(2)
            if not len_bytes:
                break

            assert len(len_bytes) == 2, "Unexpected EOF while reading filename length."
            name_len = struct.unpack("<H", len_bytes)[0]

            filename_bytes = f.read(name_len)
            assert len(filename_bytes) == name_len, "Unexpected EOF while reading filename."
            filename = filename_bytes.decode("utf-8")

            size_bytes = f.read(4)
            assert len(size_bytes) == 4, "Unexpected EOF while reading compressed size."
            comp_size = struct.unpack("<I", size_bytes)[0]

            comp_data = f.read(comp_size)
            assert len(comp_data) == comp_size, "Unexpected EOF while reading compressed data."

            try:
                decompressed = gzip.decompress(comp_data)
            except gzip.BadGzipFile:
                pytest.fail(f"Data for {filename} is not valid Gzip.")

            assert filename in expected_data, f"Found unexpected file '{filename}' in archive."
            assert decompressed == expected_data[filename], f"Content mismatch for '{filename}'. Expected {expected_data[filename]}, got {decompressed}"

            found_files.add(filename)

    expected_files = set(expected_data.keys())
    missing_files = expected_files - found_files
    assert not missing_files, f"Archive is missing expected files: {missing_files}"

    extra_files = found_files - expected_files
    assert not extra_files, f"Archive contains extra files: {extra_files}"