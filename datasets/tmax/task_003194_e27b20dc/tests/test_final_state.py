# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist():
    cpp_file = "/home/user/sequence_graph.cpp"
    sh_file = "/home/user/run_pipeline.sh"

    assert os.path.isfile(cpp_file), f"Missing required file: {cpp_file}"
    assert os.path.isfile(sh_file), f"Missing required file: {sh_file}"

    # Check if sh file is executable
    assert os.access(sh_file, os.X_OK), f"{sh_file} is not executable"

def test_openmp_usage():
    cpp_file = "/home/user/sequence_graph.cpp"
    with open(cpp_file, 'r') as f:
        content = f.read()

    assert "#pragma omp" in content, "The C++ program does not seem to use OpenMP (#pragma omp not found)."

def test_run_pipeline():
    sh_file = "/home/user/run_pipeline.sh"

    # Run the script
    result = subprocess.run(["bash", sh_file], capture_output=True, text=True, cwd="/home/user")

    assert result.returncode == 0, f"run_pipeline.sh failed with exit code {result.returncode}. Output: {result.stdout}\nError: {result.stderr}"
    assert "PASS" in result.stdout, f"run_pipeline.sh did not print 'PASS'. Output: {result.stdout}"

def test_graph_stats_output():
    stats_file = "/home/user/graph_stats.txt"
    expected_file = "/home/user/expected_stats.txt"

    assert os.path.isfile(stats_file), f"Missing generated file: {stats_file}"

    with open(stats_file, 'r') as f:
        stats_content = f.read().strip()

    with open(expected_file, 'r') as f:
        expected_content = f.read().strip()

    assert stats_content == expected_content, f"graph_stats.txt does not match expected output.\nExpected:\n{expected_content}\nGot:\n{stats_content}"