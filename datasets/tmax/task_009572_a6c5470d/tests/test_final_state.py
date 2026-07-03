# test_final_state.py

import os
import subprocess
import pytest

def test_go_output():
    path = "/home/user/go_output.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "148", f"Expected go_output.txt to contain '148', got '{content}'"

def test_mathvm_directory_and_files():
    base_dir = "/home/user/mathvm"
    assert os.path.isdir(base_dir), f"Directory {base_dir} does not exist"

    expected_files = ["vm.go", "main.go", "vm_test.go", "go.mod"]
    for f in expected_files:
        file_path = os.path.join(base_dir, f)
        assert os.path.isfile(file_path), f"Missing required file: {file_path}"

def test_benchmark_results():
    path = "/home/user/benchmark_results.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "BenchmarkEvaluate" in content, f"Expected 'BenchmarkEvaluate' in {path}"

def test_go_code_compiles_and_tests_pass():
    base_dir = "/home/user/mathvm"

    # Check if go test runs successfully
    result = subprocess.run(
        ["go", "test"],
        cwd=base_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go test' failed in {base_dir}:\n{result.stdout}\n{result.stderr}"

    # Check if main.go builds successfully
    result_build = subprocess.run(
        ["go", "build", "main.go"],
        cwd=base_dir,
        capture_output=True,
        text=True
    )
    assert result_build.returncode == 0, f"'go build main.go' failed in {base_dir}:\n{result_build.stdout}\n{result_build.stderr}"