# test_final_state.py

import os
import re
import time
import subprocess
import pytest

def test_anomalous_chunk():
    """Check that the anomalous chunk ID was correctly identified and written."""
    logs_dir = "/home/user/logs"
    anomalous_chunk_file = "/home/user/anomalous_chunk.txt"

    assert os.path.isfile(anomalous_chunk_file), f"{anomalous_chunk_file} does not exist."

    # Find the actual chunk_id in the logs that took > 5000ms
    expected_chunk_id = None
    for filename in os.listdir(logs_dir):
        if filename.endswith(".log"):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, "r") as f:
                for line in f:
                    match = re.search(r"chunk_id=(\d+)\s+processing_time=(\d+)ms", line)
                    if match:
                        chunk_id = match.group(1)
                        proc_time = int(match.group(2))
                        if proc_time > 5000:
                            expected_chunk_id = chunk_id
                            break
        if expected_chunk_id:
            break

    assert expected_chunk_id is not None, "Could not find a chunk with processing_time > 5000ms in the logs."

    with open(anomalous_chunk_file, "r") as f:
        actual_chunk_id = f.read().strip()

    assert actual_chunk_id == expected_chunk_id, f"Expected chunk_id '{expected_chunk_id}', but got '{actual_chunk_id}' in {anomalous_chunk_file}."

def test_fast_processor_exists():
    """Check that the fast_processor binary was compiled and is executable."""
    bin_path = "/home/user/src/fast_processor"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Compiled binary {bin_path} is not executable."

def test_equivalence():
    """Check that the fast_processor produces the exact same output as legacy_processor for random inputs."""
    legacy_bin = "/app/legacy_processor"
    new_bin = "/home/user/src/fast_processor"

    for i in range(5):
        random_data = os.urandom(1000)

        try:
            p_legacy = subprocess.run([legacy_bin], input=random_data, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"legacy_processor failed on random input {i}: {e}")

        try:
            p_new = subprocess.run([new_bin], input=random_data, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"fast_processor failed on random input {i}: {e}")

        assert p_legacy.stdout == p_new.stdout, f"Output mismatch between legacy and fast processor on random input {i}."

def test_speedup():
    """Check that the fast_processor achieves a speedup of at least 5.0x on the raw payloads."""
    legacy_bin = "/app/legacy_processor"
    new_bin = "/home/user/src/fast_processor"
    data_file = "/home/user/data/raw_payloads.bin"

    assert os.path.isfile(data_file), f"Data file {data_file} is missing."

    with open(data_file, "rb") as f:
        data = f.read()

    # Measure legacy processor time
    t0 = time.time()
    subprocess.run([legacy_bin], input=data, stdout=subprocess.DEVNULL, check=True)
    legacy_time = time.time() - t0

    # Measure fast processor time
    t0 = time.time()
    subprocess.run([new_bin], input=data, stdout=subprocess.DEVNULL, check=True)
    new_time = time.time() - t0

    speedup = legacy_time / new_time
    assert speedup >= 5.0, f"Speedup threshold not met: achieved {speedup:.2f}x (legacy: {legacy_time:.3f}s, new: {new_time:.3f}s), expected >= 5.0x."