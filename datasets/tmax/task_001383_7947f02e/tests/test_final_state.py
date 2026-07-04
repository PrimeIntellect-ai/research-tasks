# test_final_state.py

import os
import gzip
import struct
import subprocess
import time
import statistics
import pytest

def get_expected_metadata(root_dir):
    expected = {}
    # Python's os.walk with followlinks=True handles symlink loops safely in Python 3
    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=True):
        for f in filenames:
            if f.endswith('.wav'):
                filepath = os.path.join(dirpath, f)
                try:
                    with open(filepath, 'rb') as f_in:
                        data = f_in.read()
                        if data.startswith(b'RIFF') and data[8:12] == b'WAVE':
                            idx = 12
                            while idx + 8 <= len(data):
                                chunk_id = data[idx:idx+4]
                                chunk_size = struct.unpack('<I', data[idx+4:idx+8])[0]
                                idx += 8
                                if chunk_id == b'UTF1':
                                    utf16_data = data[idx:idx+chunk_size]
                                    text = utf16_data.decode('utf-16le')
                                    expected[f] = text
                                    break
                                idx += chunk_size
                except Exception:
                    pass
    return expected

def test_metadata_correctness():
    """Verify that the generated metadata.gz contains the correct UTF-8 strings mapped to filenames."""
    output_path = "/home/user/metadata.gz"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    try:
        with gzip.open(output_path, 'rt', encoding='utf-8') as f:
            lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(f"Failed to read {output_path} as a valid gzip UTF-8 text file: {e}")

    actual = {}
    for line in lines:
        if ': ' in line:
            fname, text = line.split(': ', 1)
            actual[fname] = text

    expected = get_expected_metadata("/app/backup_tree")

    assert len(actual) == len(expected), f"Expected {len(expected)} metadata entries, but got {len(actual)}."
    for fname, text in expected.items():
        assert fname in actual, f"Missing file {fname} in the output metadata."
        assert actual[fname] == text, f"Text mismatch for {fname}: expected '{text}', got '{actual[fname]}'."

def test_performance():
    """Verify that the C program executes within the strict runtime metric threshold."""
    binary = "/home/user/extractor"
    source = "/home/user/extractor.c"

    if not os.path.isfile(binary):
        assert os.path.isfile(source), f"Neither {binary} nor {source} was found."
        compile_cmd = ["gcc", "-O3", "-lz", source, "-o", binary]
        try:
            subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Compilation failed:\n{e.stderr}")

    assert os.access(binary, os.X_OK), f"{binary} is not executable."

    times = []
    output_path = "/home/user/metadata.gz"

    for _ in range(5):
        if os.path.exists(output_path):
            os.remove(output_path)

        start = time.perf_counter()
        try:
            subprocess.run([binary, "/app/backup_tree", output_path], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Execution of the extractor failed: {e.stderr}")
        duration = time.perf_counter() - start
        times.append(duration)

    median_time = statistics.median(times)
    threshold = 0.25
    assert median_time <= threshold, f"Median execution time {median_time:.4f}s exceeds the threshold of {threshold}s."