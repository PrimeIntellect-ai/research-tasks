# test_final_state.py

import os
import time
import subprocess
import hashlib
import pytest

def get_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_patch_file_exists():
    patch_path = "/home/user/http-parser-makefile.patch"
    assert os.path.isfile(patch_path), f"Patch file {patch_path} is missing. Step 1 requires saving the diff here."

def test_c_library_compiled():
    lib_path = "/app/vendored/http-parser-2.9.4/libhttp_parser.a"
    assert os.path.isfile(lib_path), f"C library {lib_path} was not compiled. Make sure 'make library' succeeded."

def test_rust_binary_exists():
    bin_path = "/home/user/http_analytics/target/release/http_analytics"
    assert os.path.isfile(bin_path), f"Rust binary {bin_path} not found. Did you compile the project in release mode?"

def test_execution_correctness_and_performance():
    bin_path = "/home/user/http_analytics/target/release/http_analytics"
    input_file = "/app/data/requests.log"
    output_file = "/home/user/top_urls.txt"
    expected_file = "/app/data/expected_top_urls.txt"

    assert os.path.isfile(bin_path), f"Binary {bin_path} is missing."
    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(expected_file), f"Expected output file {expected_file} is missing."

    # Remove output file if it exists to ensure a fresh run
    if os.path.exists(output_file):
        os.remove(output_file)

    start_time = time.time()
    result = subprocess.run([bin_path, input_file, output_file], capture_output=True)
    end_time = time.time()

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}.\nStderr: {result.stderr.decode()}"

    elapsed = end_time - start_time

    assert os.path.isfile(output_file), f"Output file {output_file} was not created by the application."

    expected_hash = get_sha256(expected_file)
    actual_hash = get_sha256(output_file)

    assert actual_hash == expected_hash, f"Output contents incorrect. Expected hash {expected_hash}, got {actual_hash}."

    # Verify metric threshold
    assert elapsed < 1.5, f"Execution time exceeded threshold. Elapsed: {elapsed:.3f}s, Threshold: < 1.5s"