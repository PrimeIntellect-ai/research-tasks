# test_final_state.py

import os
import subprocess
import re
import pytest

def test_rust_compilation():
    """Verify that the Rust project compiles successfully in release mode."""
    project_dir = "/home/user/shift_processor"
    assert os.path.isdir(project_dir), f"Directory missing: {project_dir}"

    result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"Cargo build failed:\n{result.stderr}"

def test_benchmark_script_exists_and_executable():
    """Verify that run_benchmark.sh exists and is executable."""
    script_path = "/home/user/run_benchmark.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_benchmark_script_execution_and_log_format():
    """Verify that running the benchmark script produces the correct log output."""
    script_path = "/home/user/run_benchmark.sh"
    input_csv = "/home/user/data/input.csv"
    log_file = "/home/user/benchmark_results.log"

    # Ensure the script and input exist before running
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.path.isfile(input_csv), f"Input CSV missing: {input_csv}"

    # Run the benchmark script
    result = subprocess.run(
        [script_path, input_csv],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"Benchmark script failed to run:\n{result.stderr}"

    # Check that the log file was created
    assert os.path.isfile(log_file), f"Log file was not created: {log_file}"

    # Read the log file and verify its contents
    with open(log_file, "r") as f:
        log_contents = f.read()

    # The expected output format is:
    # [input.csv] Processing completed. Time: <Real_Seconds>s. Valid Shifts: 2
    pattern = r"\[input\.csv\] Processing completed\. Time: \d+\.\d{2}s\. Valid Shifts: 2"

    match = re.search(pattern, log_contents)
    assert match is not None, f"Log file does not contain the expected formatted string. Contents:\n{log_contents}"