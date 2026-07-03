# test_final_state.py
import os
import subprocess
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/analyze_network.cpp"), "analyze_network.cpp is missing"
    assert os.path.isfile("/home/user/Makefile"), "Makefile is missing"
    assert os.path.isfile("/home/user/run_pipeline.sh"), "run_pipeline.sh is missing"

def test_makefile_flags():
    with open("/home/user/Makefile", "r") as f:
        content = f.read()
    assert "-O3" in content, "Makefile must include -O3 flag"
    assert "-pg" in content, "Makefile must include -pg flag"

def test_pipeline_execution_and_outputs():
    # Ensure the script is executable
    assert os.access("/home/user/run_pipeline.sh", os.X_OK), "run_pipeline.sh is not executable"

    # Run the pipeline script
    result = subprocess.run(
        ["/bin/bash", "./run_pipeline.sh"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run_pipeline.sh failed with error:\n{result.stderr}"

    # Check eigenvalue
    eigenvalue_file = "/home/user/eigenvalue.log"
    assert os.path.isfile(eigenvalue_file), f"{eigenvalue_file} was not created"

    with open(eigenvalue_file, "r") as f:
        val = f.read().strip()

    assert val == "3.0000", f"Expected eigenvalue 3.0000, got {val}"

    # Check profiling results
    profile_file = "/home/user/profile_results.txt"
    assert os.path.isfile(profile_file), f"{profile_file} was not created"

    with open(profile_file, "r") as f:
        profile_content = f.read()

    assert "Flat profile" in profile_content or "Call graph" in profile_content, \
        "profile_results.txt does not appear to contain valid gprof output"