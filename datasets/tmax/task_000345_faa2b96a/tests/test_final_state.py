# test_final_state.py

import os
import re
import pytest

def test_benchmark_cpp_exists():
    """Test that the benchmark.cpp file exists."""
    assert os.path.isfile("/home/user/benchmark.cpp"), "/home/user/benchmark.cpp does not exist."

def test_pipeline_sh_exists_and_executable():
    """Test that the pipeline.sh script exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_results_txt_exists_and_format():
    """Test that results.txt exists, has the correct format, and col-major is slower than row-major."""
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"{results_path} does not exist."

    with open(results_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 2, f"{results_path} should contain exactly 2 lines."

    row_match = re.match(r"^Row-major mean:\s+(\d+)\s+us$", content[0])
    col_match = re.match(r"^Col-major mean:\s+(\d+)\s+us$", content[1])

    assert row_match is not None, f"First line of {results_path} does not match expected format."
    assert col_match is not None, f"Second line of {results_path} does not match expected format."

    row_mean = int(row_match.group(1))
    col_mean = int(col_match.group(1))

    assert col_mean > row_mean, f"Col-major mean ({col_mean}) is not greater than Row-major mean ({row_mean})."