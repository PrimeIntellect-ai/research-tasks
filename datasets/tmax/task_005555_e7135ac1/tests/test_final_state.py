# test_final_state.py

import os
import struct
import math
import pytest

def test_metrics_out_bin_exists():
    file_path = "/home/user/metrics_out.bin"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_metrics_out_bin_content():
    file_path = "/home/user/metrics_out.bin"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_data = [
        (10, 5.0, 5.0, 0.0, 0.0),
        (11, 5.0, 5.0, 4.0, 2.0),
        (12, 7.0, 5.666666666666667, 6.0, 3.3333333333333335),
        (13, 7.0, 6.0, 6.0, 4.0),
        (14, 3.0, 5.4, 6.0, 4.4),
        (15, 3.0, 5.0, 10.0, 6.4),
        (16, 3.0, 4.6, 10.0, 7.6),
        (17, 8.0, 4.8, 10.0, 8.4),
    ]

    with open(file_path, "rb") as f:
        data = f.read()

    # Native byte order, standard alignment
    record_format = "@i4d"
    record_size = struct.calcsize(record_format)

    assert len(data) > 0, "Output file is empty."
    assert len(data) % record_size == 0, f"Output file size ({len(data)} bytes) is not a multiple of the expected record size ({record_size} bytes)."

    records = list(struct.iter_unpack(record_format, data))

    assert len(records) == len(expected_data), f"Expected {len(expected_data)} records, found {len(records)}."

    for i, (actual, expected) in enumerate(zip(records, expected_data)):
        assert actual[0] == expected[0], f"Record {i}: Expected timestamp {expected[0]}, got {actual[0]}."

        for j, field_name in enumerate(["metric1_val", "metric1_ma5", "metric2_val", "metric2_ma5"]):
            actual_val = actual[j + 1]
            expected_val = expected[j + 1]
            assert math.isclose(actual_val, expected_val, rel_tol=1e-5, abs_tol=1e-5), \
                f"Record {i} at ts={expected[0]}: Expected {field_name} to be {expected_val}, got {actual_val}."