# test_final_state.py

import os
import json
import struct
import hashlib
import pytest

BASE_DIR = "/home/user/storage_dump"
BIN_DIR = os.path.join(BASE_DIR, "binaries")
LOG_DIR = os.path.join(BASE_DIR, "logs")
ORGANIZED_DIR = "/home/user/organized_binaries"
CLEANED_LOG_DIR = "/home/user/cleaned_logs"
REPORT_FILE = "/home/user/storage_report.json"
GROUND_TRUTH_FILE = "/tmp/ground_truth.txt"

def get_ground_truth():
    truth = {}
    with open(GROUND_TRUTH_FILE, "r") as f:
        for line in f:
            key, val = line.strip().split("=")
            truth[key] = int(val)
    return truth

def test_json_report():
    truth = get_ground_truth()
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} is missing."
    with open(REPORT_FILE, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_FILE} is not valid JSON.")

    assert report.get("valid_binaries_found") == truth["valid_binaries"], "Incorrect valid_binaries_found."
    assert report.get("duplicates_replaced_with_hardlinks") == truth["hardlinks_expected"], "Incorrect duplicates_replaced_with_hardlinks."
    assert report.get("total_trivial_lines_removed") == truth["trivial_lines"], "Incorrect total_trivial_lines_removed."

def test_symlinks_created():
    assert os.path.isdir(ORGANIZED_DIR), f"Organized directory {ORGANIZED_DIR} is missing."

    valid_count = 0
    for root, dirs, files in os.walk(ORGANIZED_DIR):
        for file in files:
            path = os.path.join(root, file)
            assert os.path.islink(path), f"File {path} is not a symlink."
            target = os.readlink(path)
            assert target.startswith(BIN_DIR), f"Symlink {path} does not point to {BIN_DIR}."
            assert os.path.isfile(target), f"Symlink target {target} does not exist."

            # Verify category
            with open(target, "rb") as f:
                header = f.read(16)
                assert header[:4] == b'BKUP', f"Symlink {path} points to invalid binary."
                cat_id = struct.unpack('<I', header[4:8])[0]
                expected_dir = f"cat_{cat_id}"
                assert os.path.basename(root) == expected_dir, f"Symlink {path} is in wrong category directory."
            valid_count += 1

    truth = get_ground_truth()
    assert valid_count == truth["valid_binaries"], f"Expected {truth['valid_binaries']} symlinks, found {valid_count}."

def test_hardlinks_created():
    # Group files by content hash
    hashes = {}
    for f in os.listdir(BIN_DIR):
        if not f.endswith('.dat'):
            continue
        path = os.path.join(BIN_DIR, f)
        with open(path, "rb") as file:
            h = hashlib.sha256(file.read()).hexdigest()
        hashes.setdefault(h, []).append(path)

    for h, paths in hashes.items():
        if len(paths) > 1:
            paths.sort()
            first_inode = os.stat(paths[0]).st_ino
            for p in paths[1:]:
                assert os.stat(p).st_ino == first_inode, f"File {p} is not hardlinked to {paths[0]}."

def test_cleaned_logs():
    assert os.path.isdir(CLEANED_LOG_DIR), f"Cleaned logs directory {CLEANED_LOG_DIR} is missing."

    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.log')]
    cleaned_files = [f for f in os.listdir(CLEANED_LOG_DIR) if f.endswith('.log')]

    assert set(log_files) == set(cleaned_files), "Cleaned logs do not match original log filenames."

    for log_file in cleaned_files:
        path = os.path.join(CLEANED_LOG_DIR, log_file)
        with open(path, "r") as f:
            for line in f:
                assert not line.startswith("[DEBUG-TRIVIAL]"), f"Found trivial log in {path}."