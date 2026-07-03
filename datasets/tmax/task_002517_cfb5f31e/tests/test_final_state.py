# test_final_state.py

import os
import re
import subprocess
import pytest

def test_filter_c_fixed():
    filter_c_path = "/home/user/hybrid_image_filter/c_src/filter.c"
    assert os.path.exists(filter_c_path), f"{filter_c_path} does not exist"

    with open(filter_c_path, "r") as f:
        content = f.read()

    # Check that the bugs are fixed
    # 1. Allocation size should include sizeof(int)
    assert re.search(r"malloc\s*\(\s*width\s*\*\s*height\s*\*\s*sizeof\s*\(\s*int\s*\)\s*\)", content), "Allocation size in filter.c is still incorrect"

    # 2. Off-by-one error should be fixed (< instead of <=)
    assert not re.search(r"i\s*<=\s*width\s*\*\s*height", content), "Off-by-one error (<=) is still present in filter.c"
    assert re.search(r"i\s*<\s*width\s*\*\s*height", content), "Loop condition should use < width * height"

    # 3. Memory leak should be fixed
    assert re.search(r"free\s*\(\s*temp_buffer\s*\)", content), "temp_buffer is not freed in filter.c"

def test_run_validation_script_exists_and_executable():
    script_path = "/home/user/run_validation.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_run_validation_script_success():
    script_path = "/home/user/run_validation.sh"
    # Remove benchmark result if it exists to ensure the script creates it
    bench_result = "/home/user/benchmark_result.txt"
    if os.path.exists(bench_result):
        os.remove(bench_result)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_validation.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_benchmark_result_format():
    bench_result = "/home/user/benchmark_result.txt"
    assert os.path.exists(bench_result), f"{bench_result} was not created by the script"

    with open(bench_result, "r") as f:
        content = f.read().strip()

    assert re.match(r"^BENCHMARK_MS=\d+$", content), f"Benchmark result format is incorrect. Expected 'BENCHMARK_MS=<value>', got: {content}"