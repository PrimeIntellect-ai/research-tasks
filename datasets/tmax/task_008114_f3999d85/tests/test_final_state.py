# test_final_state.py

import os
import subprocess
import pytest

def test_joined_csv():
    """Verify joined.csv exists, has 100 lines, and correct number of columns."""
    joined_path = "/home/user/data/joined.csv"
    assert os.path.exists(joined_path), f"Missing file: {joined_path}"

    with open(joined_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"Expected 100 lines in {joined_path}, got {len(lines)}"

    for i, line in enumerate(lines):
        cols = line.split(',')
        assert len(cols) == 4, f"Line {i+1} in {joined_path} does not have 4 columns: {line}"

def test_filter_c_code():
    """Verify filter.c exists and includes cblas.h."""
    c_path = "/home/user/filter.c"
    assert os.path.exists(c_path), f"Missing file: {c_path}"

    with open(c_path, 'r') as f:
        content = f.read()

    assert "cblas.h" in content, f"cblas.h not included in {c_path}"

def test_filter_binary_linked():
    """Verify filter binary exists and is linked to openblas."""
    bin_path = "/home/user/filter"
    assert os.path.exists(bin_path), f"Missing binary: {bin_path}"
    assert os.access(bin_path, os.X_OK), f"File is not executable: {bin_path}"

    result = subprocess.run(["ldd", bin_path], capture_output=True, text=True)
    assert result.returncode == 0, f"ldd failed on {bin_path}"
    assert "openblas" in result.stdout.lower(), f"Binary {bin_path} is not linked to openblas"

def test_filtered_csv():
    """Verify filtered.csv exists, has exactly 86 lines, and 5 columns."""
    filtered_path = "/home/user/filtered.csv"
    assert os.path.exists(filtered_path), f"Missing file: {filtered_path}"

    with open(filtered_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 86, f"Expected 86 lines in {filtered_path}, got {len(lines)}"

    for i, line in enumerate(lines):
        cols = line.split(',')
        assert len(cols) == 5, f"Line {i+1} in {filtered_path} does not have 5 columns: {line}"

def test_benchmark_txt():
    """Verify benchmark.txt exists and contains a valid float > 0."""
    bench_path = "/home/user/benchmark.txt"
    assert os.path.exists(bench_path), f"Missing file: {bench_path}"

    with open(bench_path, 'r') as f:
        content = f.read().strip()

    try:
        time_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse float from {bench_path}: {content}")

    assert time_val > 0.0, f"Benchmark time must be > 0, got {time_val}"