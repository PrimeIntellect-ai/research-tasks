# test_final_state.py

import os
import csv
import struct
import pytest

def test_filtered_signal_bin():
    csv_path = "/home/user/raw_sensor_data.csv"
    bin_path = "/home/user/filtered_signal.bin"

    assert os.path.exists(bin_path), f"Missing file: {bin_path}"

    # Re-derive expected binary data
    rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['sensor_id'] == '42':
                rows.append((int(row['timestamp']), float(row['value'])))

    # Sort by timestamp ascending
    rows.sort(key=lambda x: x[0])

    # Pack values as 64-bit IEEE 754 floats
    expected_data_le = b''.join(struct.pack('<d', r[1]) for r in rows)
    expected_data_be = b''.join(struct.pack('>d', r[1]) for r in rows)
    expected_data_native = b''.join(struct.pack('d', r[1]) for r in rows)

    with open(bin_path, 'rb') as f:
        actual_data = f.read()

    assert actual_data in (expected_data_le, expected_data_be, expected_data_native), \
        "Binary data in filtered_signal.bin does not match the expected values derived from the CSV."

def test_slowest_function_txt():
    txt_path = "/home/user/slowest_function.txt"
    assert os.path.exists(txt_path), f"Missing file: {txt_path}"

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert content == "naive_median_filter", \
        f"Expected slowest function to be 'naive_median_filter', but got '{content}'"

def test_notebook_exists():
    nb_path = "/home/user/profile_workflow.ipynb"
    assert os.path.exists(nb_path), f"Missing file: {nb_path}"

def test_signal_processor_compiled():
    exe_path = "/home/user/signal_processor"
    assert os.path.exists(exe_path), f"Missing executable file: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable"