# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {script_path}"

def test_cpp_file_exists():
    cpp_path = "/home/user/detect.cpp"
    assert os.path.isfile(cpp_path), f"Missing C++ source file: {cpp_path}"

def test_pipeline_execution_and_output():
    script_path = "/home/user/pipeline.sh"
    output_path = "/home/user/top_anomalies.txt"

    # Remove output file if it exists to ensure the script generates it
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the pipeline script
    result = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}\nstderr: {result.stderr}"

    # Check if output file was created
    assert os.path.isfile(output_path), f"Output file not created by pipeline: {output_path}"

    # Verify contents
    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["4", "2", "5"]
    assert lines == expected_lines, f"Expected {expected_lines}, but got {lines} in {output_path}"