# test_final_state.py

import os
import struct
import glob

def test_extractor_c_exists():
    assert os.path.isfile("/home/user/extractor.c"), "/home/user/extractor.c does not exist."

def test_extractor_executable_exists():
    executable_path = "/home/user/extractor"
    assert os.path.isfile(executable_path), f"{executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_organize_sh_exists():
    assert os.path.isfile("/home/user/organize.sh"), "/home/user/organize.sh does not exist."

def test_inventory_sorted_log_contents():
    log_path = "/home/user/inventory_sorted.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Ensure your script creates it."

    expected_entries = []
    asset_files = glob.glob("/home/user/assets/*.bin")

    # Recompute the expected entries from the files directly
    for asset in asset_files:
        with open(asset, "rb") as f:
            data = f.read(16)
            if len(data) == 16:
                magic, proj_id, timestamp = struct.unpack("<IIQ", data)
                if magic == 0xDEADBEEF:
                    expected_entries.append((proj_id, timestamp))

    # Sort numerically by ProjectID
    expected_entries.sort(key=lambda x: x[0])
    expected_lines = [f"ProjectID: {p}, Timestamp: {t}\n" for p, t in expected_entries]

    with open(log_path, "r") as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} entries, but found {len(actual_lines)} in {log_path}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1} in {log_path}.\nExpected: {expected.strip()}\nActual: {actual.strip()}"