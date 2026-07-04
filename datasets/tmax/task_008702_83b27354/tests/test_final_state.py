# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist_and_permissions():
    c_file = "/home/user/project_subgraph.c"
    sh_file = "/home/user/query_pipeline.sh"

    assert os.path.isfile(c_file), f"{c_file} is missing."
    assert os.path.isfile(sh_file), f"{sh_file} is missing."
    assert os.access(sh_file, os.X_OK), f"{sh_file} is not executable."

def compile_c_program():
    c_file = "/home/user/project_subgraph.c"
    bin_file = "/home/user/project_subgraph"
    if not os.path.isfile(bin_file):
        result = subprocess.run(["gcc", "-O3", c_file, "-o", bin_file], capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to compile C program:\n{result.stderr}"

def run_pipeline(root, depth, min_weight):
    compile_c_program()
    cmd = ["/home/user/query_pipeline.sh", str(root), str(depth), str(min_weight)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with error:\n{result.stderr}"
    # Filter out empty lines from stdout
    output_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
    return output_lines

def test_pipeline_depth_constraint():
    # Test 1: Depth constraint (root=10, depth=2, min_weight=0)
    expected = ["10", "15", "20", "25", "30"]
    output = run_pipeline(10, 2, 0)
    assert output == expected, f"Depth constraint test failed. Expected {expected}, got {output}"

def test_pipeline_weight_filtering():
    # Test 2: Weight filtering (root=10, depth=2, min_weight=50)
    expected = ["10", "20", "30"]
    output = run_pipeline(10, 2, 50)
    assert output == expected, f"Weight filtering test failed. Expected {expected}, got {output}"

def test_pipeline_cycles_and_depth():
    # Test 3: Cycles and Depth (root=20, depth=3, min_weight=100)
    expected = ["10", "20", "30", "40", "50"]
    output = run_pipeline(20, 3, 100)
    assert output == expected, f"Cycles and depth test failed. Expected {expected}, got {output}"