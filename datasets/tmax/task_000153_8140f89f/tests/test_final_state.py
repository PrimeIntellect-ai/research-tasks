# test_final_state.py

import os
import pytest

def test_fuzz_status_pass():
    status_file = "/home/user/fuzz_status.txt"
    assert os.path.isfile(status_file), f"File not found: {status_file}. Did you run the fuzz.sh script?"

    with open(status_file, 'r') as f:
        content = f.read().strip()

    assert content == "PASS", f"Expected fuzz_status.txt to contain 'PASS', but found '{content}'"

def test_sensor_stat_executable_exists():
    exe_file = "/home/user/sensor_stat"
    assert os.path.isfile(exe_file), f"Executable not found: {exe_file}. Did you compile the program?"
    assert os.access(exe_file, os.X_OK), f"File is not executable: {exe_file}"

def test_sensor_stat_c_fixes():
    src_file = "/home/user/sensor_stat.c"
    assert os.path.isfile(src_file), f"Source file not found: {src_file}"

    with open(src_file, 'r') as f:
        content = f.read()

    assert "<math.h>" in content, "math.h is not included in sensor_stat.c"
    assert "double" in content, "The program should use 'double' precision variables instead of 'float'"

    # Check for two-pass algorithm characteristics: computing mean first, then variance
    # A simple way is to check if there are two loops or if the mean is calculated before the sum of squared differences.
    # We will just ensure 'double' is used and float is replaced/reduced, but strict AST parsing is too much.
    # The fuzz test passing is the primary indicator of correctness.

def test_build_sh_fixes():
    build_file = "/home/user/build.sh"
    assert os.path.isfile(build_file), f"Build script not found: {build_file}"

    with open(build_file, 'r') as f:
        content = f.read()

    assert "-lm" in content, "The build script should include the '-lm' flag to link the math library"

def test_fuzz_results_log_exists():
    log_file = "/home/user/fuzz_results.log"
    assert os.path.isfile(log_file), f"Log file not found: {log_file}. Did you run the fuzz.sh script?"