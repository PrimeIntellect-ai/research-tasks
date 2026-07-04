# test_final_state.py
import os
import struct
import pytest

def get_expected_clean_count():
    expected_path = '/home/user/.expected_clean_count'
    assert os.path.exists(expected_path), f"Setup file {expected_path} is missing."
    with open(expected_path, 'r') as f:
        return int(f.read().strip())

def test_summary_txt():
    expected_count = get_expected_clean_count()
    summary_path = '/home/user/summary.txt'

    assert os.path.exists(summary_path), f"The file {summary_path} does not exist."
    assert os.path.isfile(summary_path), f"The path {summary_path} is not a file."

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"The file {summary_path} does not contain a valid integer. Content: '{content}'"
    assert int(content) == expected_count, f"Expected {expected_count} clean records in {summary_path}, but found {content}."

def test_clean_data_bin_size():
    expected_count = get_expected_clean_count()
    bin_path = '/home/user/clean_data.bin'

    assert os.path.exists(bin_path), f"The file {bin_path} does not exist."
    assert os.path.isfile(bin_path), f"The path {bin_path} is not a file."

    expected_size = expected_count * 16
    actual_size = os.path.getsize(bin_path)

    assert actual_size == expected_size, f"The file {bin_path} has incorrect size. Expected {expected_size} bytes ({expected_count} records), got {actual_size} bytes."

def test_clean_data_bin_content():
    expected_count = get_expected_clean_count()
    bin_path = '/home/user/clean_data.bin'

    assert os.path.exists(bin_path), f"The file {bin_path} does not exist."

    record_format = 'iffi'
    record_size = struct.calcsize(record_format)

    with open(bin_path, 'rb') as f:
        data = f.read()

    records_read = len(data) // record_size

    # Verify that none of the records in the clean file are glitches
    # Based on the Bayesian model, a glitch is only when BOTH E1 and E2 are true
    for i in range(records_read):
        record_data = data[i * record_size : (i + 1) * record_size]
        if len(record_data) < record_size:
            break

        record_id, temp, humidity, status = struct.unpack(record_format, record_data)

        is_e1 = temp < 0.0 or temp > 50.0
        is_e2 = status != 0

        is_glitch = is_e1 and is_e2
        assert not is_glitch, f"Record with ID {record_id} was classified as clean, but it is a glitch (temp={temp}, status={status})."