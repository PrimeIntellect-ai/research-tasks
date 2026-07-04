# test_final_state.py

import os
import csv
import math
import struct
import pytest

def test_pipeline_cpp_exists():
    file_path = '/home/user/pipeline.cpp'
    assert os.path.isfile(file_path), f"{file_path} does not exist."

def test_processed_embeddings_binary():
    bin_path = '/home/user/processed_embeddings.bin'
    assert os.path.isfile(bin_path), f"{bin_path} does not exist. Did you run the pipeline?"

    expected_size = 10000 * 8 * 4
    actual_size = os.path.getsize(bin_path)
    assert actual_size == expected_size, f"{bin_path} should be exactly {expected_size} bytes, but is {actual_size} bytes."

    with open(bin_path, 'rb') as f:
        data = f.read()

    # Verify normalization of the first few and last few rows to save time, 
    # but we can do all 10000 since it's fast enough in Python.
    for i in range(10000):
        offset = i * 32
        floats = struct.unpack('<8f', data[offset:offset+32])
        norm = math.sqrt(sum(x*x for x in floats))
        # The norm should be approximately 1.0 (allow small float32 precision errors)
        assert math.isclose(norm, 1.0, rel_tol=1e-3), f"Row {i} in binary file is not normalized properly. L2 norm is {norm}."

def test_stats_txt():
    csv_path = '/home/user/raw_embeddings.csv'
    assert os.path.isfile(csv_path), "Raw data file missing."

    # Recompute the expected statistics
    v0_normalized = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            vec = [float(x) for x in row[1:9]]
            norm = math.sqrt(sum(x*x for x in vec))
            if norm > 0:
                v0_normalized.append(vec[0] / norm)
            else:
                v0_normalized.append(0.0)

    n = len(v0_normalized)
    mean_v0 = sum(v0_normalized) / n
    variance = sum((x - mean_v0)**2 for x in v0_normalized) / (n - 1)
    std_v0 = math.sqrt(variance)
    margin = 1.96 * (std_v0 / math.sqrt(n))

    expected_ci_lower = mean_v0 - margin
    expected_ci_upper = mean_v0 + margin

    stats_path = '/home/user/stats.txt'
    assert os.path.isfile(stats_path), f"{stats_path} does not exist."

    with open(stats_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    stats_dict = {}
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            stats_dict[key.strip()] = float(val.strip())

    assert 'Mean' in stats_dict, "Key 'Mean' is missing from stats.txt"
    assert 'CI_Lower' in stats_dict, "Key 'CI_Lower' is missing from stats.txt"
    assert 'CI_Upper' in stats_dict, "Key 'CI_Upper' is missing from stats.txt"

    # Allow a small tolerance for float vs double precision differences and rounding
    assert math.isclose(stats_dict['Mean'], mean_v0, abs_tol=1e-4), \
        f"Mean value incorrect. Expected ~{mean_v0:.6f}, got {stats_dict['Mean']}"
    assert math.isclose(stats_dict['CI_Lower'], expected_ci_lower, abs_tol=1e-4), \
        f"CI_Lower value incorrect. Expected ~{expected_ci_lower:.6f}, got {stats_dict['CI_Lower']}"
    assert math.isclose(stats_dict['CI_Upper'], expected_ci_upper, abs_tol=1e-4), \
        f"CI_Upper value incorrect. Expected ~{expected_ci_upper:.6f}, got {stats_dict['CI_Upper']}"