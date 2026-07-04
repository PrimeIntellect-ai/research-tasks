# test_final_state.py

import os
import stat

def test_directories_exist():
    """Check that all required directories exist."""
    base_dir = "/home/user/pipeline"
    required_dirs = ["src", "data", "build", "results"]
    for d in required_dirs:
        dir_path = os.path.join(base_dir, d)
        assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

def test_source_files_exist():
    """Check that the C source code and Makefile exist."""
    assert os.path.isfile("/home/user/pipeline/src/standardize.c"), "C source code standardize.c is missing."
    assert os.path.isfile("/home/user/pipeline/src/Makefile"), "Makefile is missing."

def test_scripts_exist():
    """Check that the shell scripts exist."""
    assert os.path.isfile("/home/user/pipeline/run_pipeline.sh"), "run_pipeline.sh is missing."
    assert os.path.isfile("/home/user/pipeline/benchmark.sh"), "benchmark.sh is missing."

def test_executable_exists():
    """Check that the compiled executable exists and is executable."""
    exe_path = "/home/user/pipeline/build/standardize"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_cleaned_matrix_output():
    """Check that the output of the standardizer matches the expected result."""
    output_path = "/home/user/pipeline/results/cleaned_matrix.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_output = (
        "-1.341641,-1.341641,0.000000\n"
        "-0.447214,-0.447214,0.000000\n"
        "0.447214,0.447214,0.000000\n"
        "1.341641,1.341641,0.000000"
    )

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_output, f"Content of {output_path} does not match expected standardized matrix."

def test_benchmark_log():
    """Check that the benchmark log exists and contains the expected success message."""
    log_path = "/home/user/pipeline/results/benchmark.log"
    assert os.path.isfile(log_path), f"Benchmark log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Benchmark completed successfully" in content, f"Expected success message not found in {log_path}."