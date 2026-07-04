# test_final_state.py

import os
import struct
import pytest

def test_mlops_eval_c_exists_and_uses_mmap():
    source_file = '/home/user/mlops_eval.c'
    assert os.path.exists(source_file), f"Source file {source_file} does not exist."
    with open(source_file, 'r') as f:
        code = f.read()
    assert 'mmap' in code, "The string 'mmap' was not found in the source code."

def test_metrics_log_format_and_values():
    log_file = '/home/user/metrics.log'
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    file_size = os.path.getsize(log_file)
    assert file_size > 0, f"Log file {log_file} is empty."
    assert file_size % 24 == 0, f"Log file {log_file} size ({file_size}) is not a multiple of 24 bytes."

    # Recompute expected metrics from the actual binary files
    truth_file = '/home/user/artifacts/truth.bin'
    inference_file = '/home/user/artifacts/inference.bin'

    assert os.path.exists(truth_file), f"{truth_file} missing."
    assert os.path.exists(inference_file), f"{inference_file} missing."

    with open(truth_file, 'rb') as f:
        truth_data = f.read()
    with open(inference_file, 'rb') as f:
        inference_data = f.read()

    num_floats = 2500000
    assert len(truth_data) == num_floats * 4
    assert len(inference_data) == num_floats * 4

    # Read floats and compute exact metrics
    # Using struct.unpack iterator or direct unpack
    truth_floats = struct.unpack(f'<{num_floats}f', truth_data)
    inference_floats = struct.unpack(f'<{num_floats}f', inference_data)

    total_ae = 0.0
    max_ae = 0.0

    for t, i in zip(truth_floats, inference_floats):
        diff = abs(t - i)
        total_ae += diff
        if diff > max_ae:
            max_ae = diff

    expected_mae = total_ae / num_floats
    expected_max_ae = max_ae

    # Verify the last record in the log file
    with open(log_file, 'rb') as f:
        f.seek(-24, os.SEEK_END)
        record = f.read(24)

    timestamp, mae, actual_max_ae, time_us = struct.unpack('<QffQ', record)

    assert abs(mae - expected_mae) < 1e-4, f"MAE mismatch. Expected approx {expected_mae}, got {mae}"
    assert abs(actual_max_ae - expected_max_ae) < 1e-4, f"MaxAE mismatch. Expected approx {expected_max_ae}, got {actual_max_ae}"
    assert time_us > 0, f"Compute time should be greater than 0, got {time_us}"
    assert timestamp > 0, f"Timestamp should be greater than 0, got {timestamp}"