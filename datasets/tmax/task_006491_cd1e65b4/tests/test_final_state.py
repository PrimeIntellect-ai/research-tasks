# test_final_state.py

import os
import re
import subprocess
import pytest

def test_directories_exist():
    """Check if the required directories exist."""
    directories = [
        '/home/user/src',
        '/home/user/bin',
        '/home/user/results'
    ]
    for d in directories:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_cpp_source():
    """Check if the C++ source file exists and contains required keywords."""
    src_file = '/home/user/src/density_omp.cpp'
    assert os.path.isfile(src_file), f"Source file {src_file} does not exist."

    with open(src_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '#pragma omp' in content, f"{src_file} does not contain OpenMP pragmas."
    assert 'hdf5.h' in content or 'H5Cpp.h' in content, f"{src_file} does not contain HDF5 includes."

def test_executable():
    """Check if the compiled executable exists, is executable, and is linked correctly."""
    exe_file = '/home/user/bin/density_omp'
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

    # Check linkage using ldd
    result = subprocess.run(['ldd', exe_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run ldd on {exe_file}."

    output = result.stdout.lower()
    assert 'libhdf5' in output, f"{exe_file} is not linked against libhdf5."
    assert 'libgomp' in output, f"{exe_file} is not linked against OpenMP (libgomp)."

def test_bash_script():
    """Check if the bash script exists, is executable, and contains resampling logic."""
    script_file = '/home/user/bin/benchmark.sh'
    assert os.path.isfile(script_file), f"Bash script {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"File {script_file} is not executable."

    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '1000' in content, f"{script_file} does not seem to contain the 1000 resamples logic."

def test_histogram_out():
    """Check if the histogram output exists, has 100 lines, and sums to 1,000,000."""
    hist_file = '/home/user/results/histogram.out'
    assert os.path.isfile(hist_file), f"Histogram output {hist_file} does not exist."

    with open(hist_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"Expected 100 lines in {hist_file}, got {len(lines)}."

    total_sum = 0
    for i, line in enumerate(lines):
        try:
            val = int(line)
            total_sum += val
        except ValueError:
            pytest.fail(f"Line {i+1} in {hist_file} is not a valid integer: '{line}'")

    assert total_sum == 1000000, f"Expected sum of histogram counts to be 1000000, got {total_sum}."

def test_ci_txt():
    """Check if the CI output file exists and matches the required format."""
    ci_file = '/home/user/results/ci.txt'
    assert os.path.isfile(ci_file), f"CI output {ci_file} does not exist."

    with open(ci_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    pattern = r'^Mean CI: \[\d+\.\d{2}, \d+\.\d{2}\]$'
    assert re.match(pattern, content), f"Content of {ci_file} ('{content}') does not match expected format 'Mean CI: [lower, upper]'."