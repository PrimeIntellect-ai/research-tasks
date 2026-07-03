# test_final_state.py
import os
import struct
import glob
import pytest

def test_storage_dump_deleted():
    assert not os.path.exists("/home/user/storage_dump"), "/home/user/storage_dump was not deleted."

def test_metrics_converter_project_exists():
    assert os.path.isdir("/home/user/metrics_converter"), "/home/user/metrics_converter directory is missing."

def test_no_intermediate_files():
    # Check for .log and .csv files in /home/user (non-recursive)
    logs = glob.glob("/home/user/*.log")
    csvs = glob.glob("/home/user/*.csv")
    assert len(logs) == 0, f"Found leftover .log files in /home/user: {logs}"
    assert len(csvs) == 0, f"Found leftover .csv files in /home/user: {csvs}"

def test_metrics_bin_validity():
    bin_path = "/home/user/metrics.bin"
    assert os.path.isfile(bin_path), f"{bin_path} not found."

    with open(bin_path, "rb") as f:
        data = f.read()

    assert len(data) >= 4, "File is too small to contain a header."
    magic = data[:4]
    assert magic == b"METR", f"Invalid magic bytes: expected b'METR', got {magic}"

    payload = data[4:]
    assert len(payload) % 17 == 0, f"Payload length {len(payload)} is not a multiple of 17 bytes."

    records_count = len(payload) // 17
    found_sync = False
    found_heavy = False

    for i in range(records_count):
        chunk = payload[i * 17 : (i + 1) * 17]
        ts, cpu, ram, disk = struct.unpack(">QBII", chunk)

        if ts == 1710009999 and cpu == 12 and ram == 4096 and disk == 250:
            found_sync = True
        if ts == 1710010005 and cpu == 99 and ram == 65536 and disk == 1900:
            found_heavy = True

    assert found_sync, "Could not find expected specific record 1 (Sync) in the binary."
    assert found_heavy, "Could not find expected specific record 2 (Heavy load) in the binary."