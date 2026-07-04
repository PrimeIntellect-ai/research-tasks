# test_final_state.py

import os
import zlib
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/build_prep.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_log_file_exists():
    log_path = "/home/user/prep_results.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

def test_log_contents():
    log_path = "/home/user/prep_results.log"
    assert os.path.isfile(log_path), "Log file missing."

    with open(log_path, "r") as f:
        log_content = f.read()

    # Parse log file into a dictionary
    results = {}
    for line in log_content.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            results[key.strip()] = val.strip()

    # 1. Check HIGHEST_VERSION
    libs_path = "/home/user/deps/libs.txt"
    assert os.path.isfile(libs_path), f"{libs_path} is missing."
    with open(libs_path, "r") as f:
        versions = f.read().strip().split('\n')

    # Simple semantic version sorting
    def parse_version(v):
        return tuple(int(x) for x in v.split('.'))

    expected_version = max(versions, key=parse_version)
    assert "HIGHEST_VERSION" in results, "HIGHEST_VERSION missing from log."
    assert results["HIGHEST_VERSION"] == expected_version, f"Expected HIGHEST_VERSION {expected_version}, got {results['HIGHEST_VERSION']}."

    # 2. Check BUFFER_SIZE
    expr_path = "/home/user/deps/config.expr"
    assert os.path.isfile(expr_path), f"{expr_path} is missing."
    with open(expr_path, "r") as f:
        expr = f.read().strip()

    expected_buffer_size = str(eval(expr))
    assert "BUFFER_SIZE" in results, "BUFFER_SIZE missing from log."
    assert results["BUFFER_SIZE"] == expected_buffer_size, f"Expected BUFFER_SIZE {expected_buffer_size}, got {results['BUFFER_SIZE']}."

    # 3. Check PAYLOAD_ADLER32
    payload_path = "/home/user/deps/payload.dat"
    assert os.path.isfile(payload_path), f"{payload_path} is missing."
    with open(payload_path, "rb") as f:
        payload_data = f.read()

    expected_adler32 = f"{zlib.adler32(payload_data) & 0xffffffff:08x}"
    assert "PAYLOAD_ADLER32" in results, "PAYLOAD_ADLER32 missing from log."
    assert results["PAYLOAD_ADLER32"] == expected_adler32, f"Expected PAYLOAD_ADLER32 {expected_adler32}, got {results['PAYLOAD_ADLER32']}."

    # 4. Check BENCHMARK_TIME
    assert "BENCHMARK_TIME" in results, "BENCHMARK_TIME missing from log."
    try:
        benchmark_time = float(results["BENCHMARK_TIME"])
        assert benchmark_time > 0, "BENCHMARK_TIME must be greater than 0."
    except ValueError:
        pytest.fail(f"BENCHMARK_TIME is not a valid float: {results['BENCHMARK_TIME']}")