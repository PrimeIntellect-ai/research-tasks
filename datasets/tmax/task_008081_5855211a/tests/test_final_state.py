# test_final_state.py

import os
import pytest

def test_parquet_file_created_and_valid():
    parquet_path = "/home/user/clean_sensors.parquet"
    assert os.path.isfile(parquet_path), f"The file {parquet_path} was not created."

    # Check for Parquet magic bytes (PAR1) at the beginning and end of the file
    with open(parquet_path, "rb") as f:
        header = f.read(4)
        f.seek(-4, 2)
        footer = f.read(4)

    assert header == b"PAR1", f"File {parquet_path} is not a valid Parquet file (missing PAR1 header)."
    assert footer == b"PAR1", f"File {parquet_path} is not a valid Parquet file (missing PAR1 footer)."

def test_metrics_log_created_and_correct():
    log_path = "/home/user/metrics.log"
    assert os.path.isfile(log_path), f"The file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "0.1197", f"Expected metrics.log to contain '0.1197', but found '{content}'."