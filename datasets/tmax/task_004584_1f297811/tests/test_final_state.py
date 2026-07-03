# test_final_state.py

import os
import time
import subprocess
import pytest

def test_crash_frame():
    path = "/home/user/crash_frame.txt"
    assert os.path.isfile(path), f"Missing output file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "142", f"Expected crash frame to be '142', got '{content}'"

def test_fixed_tool_exists():
    path = "/home/user/fixed_tool"
    assert os.path.isfile(path), f"Missing compiled executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_fixed_tool_performance(tmp_path):
    executable = "/home/user/fixed_tool"
    assert os.path.isfile(executable), "Executable not found"

    # Create a large test data file
    test_data_path = "/app/large_test_data.dat"
    if not os.path.exists(test_data_path):
        with open(test_data_path, "w") as f:
            # Write 1,000,000 lines of dummy telemetry data
            f.write("10\n" * 1000000)

    # Set up environment for the legacy library
    env = os.environ.copy()
    legacy_lib_path = "/opt/legacy_libs"
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{legacy_lib_path}:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = legacy_lib_path

    # Measure runtime
    start_time = time.perf_counter()
    result = subprocess.run(
        [executable, test_data_path],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )
    end_time = time.perf_counter()
    runtime = end_time - start_time

    assert result.returncode == 0, f"Executable crashed or failed with return code {result.returncode}. Stderr: {result.stderr}"

    threshold = 0.2
    assert runtime <= threshold, f"Performance metric failed: Runtime was {runtime:.4f}s, threshold is <= {threshold}s"