# test_final_state.py

import os
import subprocess
import time
import struct
import pytest

def test_execution_time_and_correctness():
    """
    Validates that the compiled C++ binary runs within the execution time threshold
    and produces the mathematically correct output.
    """
    binary_path = "/home/user/audio_processor/build/audio_processor"
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}"

    output_path = "/home/user/output.bin"
    assert os.path.exists(output_path), f"Output file not found at {output_path}"

    # 1. Measure runtime of the optimized binary
    test_output_path = "/home/user/test_output.bin"
    start_time = time.time()
    result = subprocess.run(
        [binary_path, "/app/dataset.bin", test_output_path],
        capture_output=True
    )
    end_time = time.time()

    assert result.returncode == 0, f"Binary execution failed with error: {result.stderr.decode()}"

    execution_time = end_time - start_time
    assert execution_time <= 0.15, f"Execution time {execution_time:.4f}s exceeds the required threshold of 0.15s"

    # 2. Validate correctness of the generated output file
    # Determine struct layout based on file size (12 bytes packed, or 16 bytes if 8-byte aligned)
    file_size = os.path.getsize(output_path)
    assert file_size > 0, "Output file is empty"

    if file_size % 16 == 0:
        record_size = 16
        fmt = "i f 4s 4x"
    elif file_size % 12 == 0:
        record_size = 12
        fmt = "i f 4s"
    else:
        pytest.fail(f"Output file size {file_size} is not a multiple of expected struct size (12 or 16 bytes).")

    with open(output_path, "rb") as f:
        actual_data = f.read()

    actual_records = []
    for i in range(0, len(actual_data), record_size):
        chunk = actual_data[i:i+record_size]
        if len(chunk) < record_size:
            break
        _id, val, padding = struct.unpack(fmt, chunk)
        actual_records.append((_id, val))

    # Check if threshold of 42 was applied
    for _id, val in actual_records:
        assert val >= 42.0, f"Found record with value {val} < 42.0. Threshold filter not applied correctly."

    # Check if sorted in descending order
    for i in range(1, len(actual_records)):
        assert actual_records[i-1][1] >= actual_records[i][1], "Output records are not sorted in descending order by value."

    # Compare with expected counts from dataset.bin
    with open("/app/dataset.bin", "rb") as f:
        dataset_data = f.read()

    expected_count = 0
    for i in range(0, len(dataset_data), record_size):
        chunk = dataset_data[i:i+record_size]
        if len(chunk) < record_size:
            break
        _, val, _ = struct.unpack(fmt, chunk)
        if val >= 42.0:  # Threshold from config.wav
            expected_count += 1

    assert len(actual_records) == expected_count, f"Output file has {len(actual_records)} records, expected {expected_count} based on threshold 42.0."